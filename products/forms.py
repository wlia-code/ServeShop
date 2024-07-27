from django import forms
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from .widgets import CustomClearableFileInput
from .models import Product, Category, Testimonial


class ProductForm(forms.ModelForm):
    """Form for Product model with all fields."""
    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        """Initialize form and set category choices."""
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def clean_price(self):
        """Ensure price is greater than zero."""
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('The price must be greater than zero.')
        return price


class ContactForm(forms.Form):
    """Form for user contact information."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        """Send the form data via email."""
        try:
            send_mail(
                self.cleaned_data['subject'],
                self.cleaned_data['message'],
                self.cleaned_data['email'],
                ['etherumm@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            # Handle the error appropriately
            print(f"Error sending email: {e}")
            raise ValidationError(
                'Error sending message. Please try again later.'
            )


class TestimonialForm(forms.ModelForm):
    """Form for Testimonial model."""
    class Meta:
        model = Testimonial
        fields = ['text', 'rating', 'image']
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'Write your testimonial here...'}
            ),
            'rating': forms.Select(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'image': forms.ClearableFileInput(),
        }

    def clean_text(self):
        """Ensure testimonial text has at least 10 characters."""
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise ValidationError('The text must be at least 10 characters.')
        return text
