from django.contrib import admin
from .models import UserProfile, ProductReview

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer_name', 'rating', 'created_at', 'approved']
    list_filter = ['created_at', 'rating', 'approved']
    search_fields = ['comment', 'customer_name', 'product__name']
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)
    approve_reviews.short_description = "Approve selected reviews"

admin.site.register(UserProfile)
