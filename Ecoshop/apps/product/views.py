import random
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import addToCartForm
from .models import Product, Category

from apps.cart.cart import Cart


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'product/search.html', {'products': products, 'query': query})


def product(request, category_slug, product_slug):
    cart=Cart(request)
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method=='POST':
        form=addToCartForm(request.POST)

        if form.is_valid():
            quantity=form.cleaned_data['quantity']
            cart.add(product_id=product.id,quantity=quantity,update_quantity=False)

            messages.success(request,'Product added to cart')

            return redirect('product',category_slug=category_slug,product_slug=product_slug)
    else:
        form=addToCartForm()

    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)
    return render(request, 'product/product-page.html', {'form':form,'product': product,'cart':cart,'similar_produts': similar_products})


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'product/category.html', {'category': category})

