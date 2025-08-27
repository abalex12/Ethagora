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
    path('complete-profile/', views.complete_profile, name='complete_profile'),


    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify-email'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('resend-verification/', views.resend_verification, name='resend-verification'),

    
    # Seller pages
    path('create-listing/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/edit', views.edit_listing, name='listing_edit'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path("listing/<int:pk>/status/<str:new_status>/", views.set_listing_status, name="listing_set_status"),

    
    # AJAX endpoints
    path('api/subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/filter-listings/', views.filter_listings, name='filter_listings'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),

    path('account/settings/', views.account_settings, name='account-settings'),
    path('account/delete/', views.delete_account_request, name='delete-account'),
    path('account/delete/confirm/', views.delete_account_confirm, name='delete-account-confirm'),

]