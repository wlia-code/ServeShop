from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


"""
The project structure and some of the
backend code were adapted from the Code Institute's
"Boutique Ado" walk-through project.
(https://codeinstitute.net)

"""


class Category(models.Model):
    """Category model to classify products."""
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """Return the friendly name of the category."""
        return self.friendly_name


class Product(models.Model):
    """Product model with various attributes."""
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # noqa
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Testimonial(models.Model):
    """Testimonial model for user feedback."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    review = models.CharField(max_length=255, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)  # noqa
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.user.username}"


class ContactRequest(models.Model):
    """Model for storing user contact requests."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ContactRequest from {self.user.username} - {self.subject}"
