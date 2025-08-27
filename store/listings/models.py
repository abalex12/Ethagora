from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import cloudinary
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    telegram_username = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    email_verified = models.BooleanField(default=False)  # Added this field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'SubCategories'
        ordering = ['name']
        unique_together = ['category', 'slug']
    
    def __str__(self):
        return f"{self.category.name} → {self.name}"

class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
   
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('removed', 'Removed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=200)
    contact_telegram = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    view_count = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})
    
    def get_primary_image(self):
        primary_image = self.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image
        return self.images.first()

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    # Replace ImageField with CloudinaryField
    image = CloudinaryField(
        'image',
        folder='listings',  # Organize images in folders
        transformation={
            'quality': 'auto:good',
            'fetch_format': 'auto',
            'width': 800,
            'height': 600,
            'crop': 'limit'
        }
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.listing.title}"
    
    def get_thumbnail_url(self):
        """Get a thumbnail version of the image"""
        if self.image:
            return cloudinary.CloudinaryImage(str(self.image)).build_url(
                width=300,
                height=200,
                crop='fill',
                quality='auto:good',
                fetch_format='auto'
            )
        return None
    
    def get_medium_url(self):
        """Get a medium-sized version of the image"""
        if self.image:
            return cloudinary.CloudinaryImage(str(self.image)).build_url(
                width=600,
                height=400,
                crop='limit',
                quality='auto:good',
                fetch_format='auto'
            )
        return None