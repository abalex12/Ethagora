from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Listing, Category, SubCategory, ListingImage
from .forms import SellerSignUpForm, ListingForm, ListingSearchForm
from .forms import ListingImageFormSet


def home(request):
    # Get recent listings
    recent_listings = Listing.objects.filter(status='available')[:8]
    featured=Listing.objects.filter(status='available')[:3]
    categories = Category.objects.all()
    
    context = {
        'recent_listings': recent_listings,
        'featured':featured,
        'categories': categories,
    }
    return render(request, 'listings/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # User can login but email not verified
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SellerSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def listings_view(request):
    form = ListingSearchForm(request.GET)
    listings = Listing.objects.filter(status='available')
    
    # Apply filters
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        subcategory = form.cleaned_data.get('subcategory')
        condition = form.cleaned_data.get('condition')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        sort_by = form.cleaned_data.get('sort_by')
        
        if search:
            listings = listings.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if category:
            listings = listings.filter(category=category)
        if subcategory:
            listings = listings.filter(subcategory=subcategory)
        if condition:
            listings = listings.filter(condition=condition)
        if min_price:
            listings = listings.filter(price__gte=min_price)
        if max_price:
            listings = listings.filter(price__lte=max_price)
            
        # Sorting
        if sort_by == 'oldest':
            listings = listings.order_by('created_at')
        elif sort_by == 'price_low':
            listings = listings.order_by('price')
        elif sort_by == 'price_high':
            listings = listings.order_by('-price')
        else:  # newest (default)
            listings = listings.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    listings = paginator.get_page(page_number)
    
    context = {
        'listings': listings,
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'listings/listings.html', context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    # Increment view count
    listing.view_count += 1
    listing.save(update_fields=['view_count'])
    
    # Get related listings
    related_listings = Listing.objects.filter(
        category=listing.category, 
        status='available'
    ).exclude(pk=pk)[:4]
    
    context = {
        'listing': listing,
        'related_listings': related_listings,
    }
    return render(request, 'listings/listing_detail.html', context)


from django.forms import modelformset_factory

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        formset = ListingImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            
            instances = formset.save(commit=False)
            for instance in instances:
                instance.listing = listing
                instance.save()
            
            # Ensure only one primary image exists
            primary_images = listing.images.filter(is_primary=True)
            if primary_images.count() > 1:
                first = primary_images.first()
                listing.images.exclude(pk=first.pk).update(is_primary=False)
            
            messages.success(request, 'Listing created successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
        formset = ListingImageFormSet(queryset=ListingImage.objects.none())
    
    context = {
        'form': form,
        'formset': formset,
        'is_create': True,
    }
    return render(request, 'listings/create_listing.html', context)

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        formset = ListingImageFormSet(request.POST, request.FILES, instance=listing)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            # Ensure only one primary image exists
            primary_images = listing.images.filter(is_primary=True)
            if primary_images.count() > 1:
                first = primary_images.first()
                listing.images.exclude(pk=first.pk).update(is_primary=False)
            
            messages.success(request, 'Listing updated successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
        formset = ListingImageFormSet(instance=listing)
    
    context = {
        'form': form,
        'formset': formset,
        'listing': listing,
        'is_create': False,
    }
    return render(request, 'listings/create_listing.html', context)


@login_required
def my_listings(request):
    listings = request.user.listings.all()
    return render(request, 'listings/my_listings.html', {'listings': listings})
    
def set_listing_status(request, pk, new_status):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    valid_statuses = ["available", "sold", "removed"]

    if new_status.lower() in valid_statuses:
        listing.status = new_status.lower()
        listing.save(update_fields=["status"])
        messages.success(request, f"Listing status updated to '{new_status}'.")
    else:
        messages.error(request, "Invalid status selected.")

    return redirect("my_listings")

# AJAX Views
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name','icon')
    return JsonResponse(list(subcategories), safe=False)


def filter_listings(request):
    """AJAX endpoint for dynamic filtering"""
    form = ListingSearchForm(request.GET)
    listings = Listing.objects.filter(status='available')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        subcategory = form.cleaned_data.get('subcategory')
        condition = form.cleaned_data.get('condition')
        location = form.cleaned_data.get('city')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        sort_by = form.cleaned_data.get('sort_by')
        
        if search:
            listings = listings.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if category:
            listings = listings.filter(category=category)
        if subcategory:
            listings = listings.filter(subcategory=subcategory)
        if condition:
            listings = listings.filter(condition=condition)
        if location:
            listing = listing.filter(location=location)
        if min_price:
            listings = listings.filter(price__gte=min_price)
        if max_price:
            listings = listings.filter(price__lte=max_price)
        
            
        # Sorting
        if sort_by == 'oldest':
            listings = listings.order_by('created_at')
        elif sort_by == 'price_low':
            listings = listings.order_by('price')
        elif sort_by == 'price_high':
            listings = listings.order_by('-price')
        else:
            listings = listings.order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(listings, 12)
    listings_page = paginator.get_page(page)
    
    listings_html = render(request, 'listings/partials/listing_cards.html', {
        'listings': listings_page
    }).content.decode('utf-8')
    
    return JsonResponse({
        'listings_html': listings_html,
        'has_next': listings_page.has_next(),
        'has_previous': listings_page.has_previous(),
        'total_count': paginator.count,
    })
from django.views.decorators.cache import cache_page

import json
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page


@require_http_methods(["GET"])
def search_suggestions(request):
    """
    AJAX view to provide search suggestions based on categories, subcategories, and products
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    suggestions = []
    
    try:
        # Search categories - Remove is_active filter if it doesn't exist
        try:
            categories = Category.objects.filter(
                name__icontains=query
            ).distinct()[:4]
        except:
            # Fallback if is_active field doesn't exist
            categories = Category.objects.filter(
                name__icontains=query
            ).distinct()[:4]
        
        for category in categories:
            suggestions.append({
                'name': category.name,
                'type': 'category',
                'type_display': 'Category',
                'url': f"{reverse('listings')}?category={category.id}",
                'category_id': category.id,
                'subcategory_id': None
            })
        
        # Search subcategories - Remove is_active filters if they don't exist
        try:
            subcategories = SubCategory.objects.filter(
                name__icontains=query
            ).select_related('category').distinct()[:5]
        except:
            # Fallback if is_active field doesn't exist
            subcategories = SubCategory.objects.filter(
                name__icontains=query
            ).select_related('category').distinct()[:5]
        
        for subcategory in subcategories:
            suggestions.append({
                'name': f"{subcategory.name}",
                'type': 'subcategory', 
                'type_display': f"in {subcategory.category.name}",
                'url': f"{reverse('listings')}?category={subcategory.category.id}&subcategory={subcategory.id}",
                'category_id': subcategory.category.id,
                'subcategory_id': subcategory.id
            })
        
        # Search product names (from listings) - if Listing model exists
        try:
            products = Listing.objects.filter(
                title__icontains=query
            ).select_related('category', 'subcategory').distinct()[:3]
            
            for product in products:
                url = f"{reverse('listings')}?category={product.category.id}"
                if hasattr(product, 'subcategory') and product.subcategory:
                    url += f"&subcategory={product.subcategory.id}"
                
                suggestions.append({
                    'name': product.title,
                    'type': 'product',
                    'type_display': f"Product in {product.category.name}",
                    'url': url,
                    'category_id': product.category.id,
                    'subcategory_id': product.subcategory.id if hasattr(product, 'subcategory') and product.subcategory else None
                })
        except:
            # If Listing model doesn't exist or has different structure, skip products
            pass
        
        # Remove duplicates based on URL and limit results
        unique_suggestions = []
        seen_urls = set()
        
        for suggestion in suggestions:
            if suggestion['url'] not in seen_urls:
                unique_suggestions.append(suggestion)
                seen_urls.add(suggestion['url'])
        
        # Limit to 8 suggestions total
        unique_suggestions = unique_suggestions[:8]
        
        # Debug: Add some test data if no suggestions found
        if not unique_suggestions and query:
            # For debugging - you can remove this after confirming it works
            unique_suggestions.append({
                'name': f"Search results for '{query}'",
                'type': 'search',
                'type_display': 'General Search',
                'url': f"{reverse('listings')}?search={query}",
                'category_id': None,
                'subcategory_id': None
            })
        
        return JsonResponse({
            'suggestions': unique_suggestions,
            'total': len(unique_suggestions),
            'query': query  # For debugging
        })
        
    except Exception as e:
        # Better error handling for debugging
        return JsonResponse({
            'suggestions': [],
            'error': str(e),
            'query': query
        })



def privacy_policy(request):
    return render(request, "listings/privacy_policy.html")

def terms_of_service(request):
    return render(request, "listings/terms_of_service.html")
