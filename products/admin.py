from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Category, ProductReview, Wishlist, Testimonial, ContactRequest

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    actions = ['approve_testimonials']

    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
        for testimonial in queryset:
            send_mail(
                'Your Testimonial is Approved',
                'Your testimonial has been approved and is now visible on the site.',
                settings.DEFAULT_FROM_EMAIL,
                [testimonial.user.email],
                fail_silently=False,
            )
    approve_testimonials.short_description = "Approve selected testimonials"


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(ProductReview)
admin.site.register(Wishlist)
admin.site.register(ContactRequest)