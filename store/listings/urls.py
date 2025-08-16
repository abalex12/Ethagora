from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('listings/', views.listings_view, name='listings'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    
    # Authentication
    # Allauth routes
    path('accounts/', include('allauth.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Seller pages
    path('create-listing/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/edit', views.edit_listing, name='listing_edit'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path("listing/<int:pk>/status/<str:new_status>/", views.set_listing_status, name="listing_set_status"),

    
    # AJAX endpoints
    path('api/subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/filter-listings/', views.filter_listings, name='filter_listings'),
]