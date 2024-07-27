from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User  # noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    Product, Category, Wishlist, Testimonial, ContactRequest
)
from .forms import ProductForm, ContactForm, TestimonialForm
from profiles.models import ProductReview

"""
The project structure and some of the
backend code were adapted from the Code Institute's
"Boutique Ado" walk-through project.
(https://codeinstitute.net)
"""


def all_products(request):
    """View to show all products, including sorting and search queries."""
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse('products'))

            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """View to show individual product details."""
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(
        product=product, approved=True
    ).order_by('-created_at')

    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'products/product_detail.html', context)


def all_reviews(request, product_id):
    """View to show all reviews for a specific product."""
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(
        product=product, approved=True
    ).order_by('-created_at')

    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'products/all_reviews.html', context)


@login_required
def add_product(request):
    """Add a product to the store."""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to add product. Ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit a product in the store."""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product. Ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store."""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_to_wishlist(request, product_id):
    """Add a product to the user's wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user, product=product
    )

    if created:
        messages.success(request, f'Added {product.name} to your wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')

    return redirect('product_detail', product_id=product.id)


@login_required
def view_wishlist(request):
    """View the user's wishlist."""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {
        'wishlist_items': wishlist_items
    })


@login_required
@require_POST
def remove_from_wishlist_ajax(request):
    """Remove a product from the user's wishlist via AJAX."""
    product_id = request.POST.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
        Wishlist.objects.filter(user=request.user, product=product).delete()
        return JsonResponse({'success': True})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found.'})


@login_required
def submit_testimonial(request):
    """Submit a testimonial."""
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(
                request, "Thank you for submitting your testimonial."
                         " It will be reviewed by an admin soon."
            )
            return redirect('home')
        else:
            messages.error(
                request, "The text must be at least 10 characters"
            )
    else:
        form = TestimonialForm()
    return render(request, "products/submit_testimonial.html", {"form": form})


def submit_contact_request(request):
    """Submit a contact request."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.send_email()
                request.session["user_name"] = form.cleaned_data["name"]
                return redirect("success_url")
            except Exception as e:
                messages.error(
                    request, f"Failed to send email: {str(e)}"
                )
                return render(
                    request, "products/submit_contact_request.html",
                    {"form": form}
                )
        else:
            return render(
                request, "products/submit_contact_request.html",
                {"form": form}
            )
    else:
        form = ContactForm()
        return render(
            request, "products/submit_contact_request.html",
            {"form": form}
        )


def success(request):
    """Render a success page."""
    return render(request, "products/success.html")
