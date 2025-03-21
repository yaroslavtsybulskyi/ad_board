from django.contrib import admin

from .models import UserProfile, Ad, Category, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email', 'address')
    search_fields = ('user__username', 'email', 'phone_number')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active_ads_count')
    search_fields = ('name', 'description')


@admin.register(Ad)
class AdAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'created_at', 'updated_at',
                    'is_active', 'user', 'category', 'short_description')
    search_fields = ('title', 'description', 'user__user__username', 'category__name')
    list_filter = ('is_active', 'category')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'user', 'ad')
    search_fields = ('content', 'user__username', 'ad__title')
    ordering = ('-created_at',)
