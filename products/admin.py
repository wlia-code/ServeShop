from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from .models import (
    Product, Category, ProductReview, Wishlist, Testimonial, ContactRequest
)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku', 'name', 'category', 'price', 'rating', 'image'
    )
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name', 'name'
    )


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'rating', 'approved', 'created_at', 'image_tag')
    list_filter = ('approved', 'created_at')
    actions = ['approve_testimonials']

    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
        for testimonial in queryset:
            send_mail(
                'Your Testimonial is Approved',
                'Your testimonial has been approved and is now visible '
                'on the site.',
                settings.DEFAULT_FROM_EMAIL,
                [testimonial.user.email],
                fail_silently=False,
            )
    approve_testimonials.short_description = "Approve selected testimonials"

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 45px; height:45px;" />'.format(
                    obj.image.url
                )
            )
        return None
    image_tag.short_description = 'Image'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(ProductReview)
admin.site.register(Wishlist)
admin.site.register(ContactRequest)
