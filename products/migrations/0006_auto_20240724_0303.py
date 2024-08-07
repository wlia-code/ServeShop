# Generated by Django 3.2.25 on 2024-07-24 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_contactrequest_productreview_testimonial_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='testimonials/'),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='review',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
