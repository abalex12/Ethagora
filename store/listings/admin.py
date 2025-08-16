from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, SubCategory, Listing, ListingImage


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'location', 'created_at')
    list_filter = ('location', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('telegram_username', 'phone', 'location')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'created_at')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'condition', 'status', 'view_count', 'created_at')
    list_filter = ('category', 'condition', 'status', 'created_at')
    search_fields = ('title', 'description')
    inlines = [ListingImageInline]