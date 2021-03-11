from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib import messages

from apps.product.models import Product
from .forms import ProductForm
from .models import Vendor


def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            vendor = Vendor.objects.create(name=user.username, created_by=user)
            messages.success(request,'Vendor account created successfully!')
            return redirect('vendor_admin')
    else:
        form = UserCreationForm()
    return render(request, 'vendor/become_vendor.html', {'form': form})


@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    return render(request, 'vendor/vendor-admin.html', {'vendor': vendor, 'products': products})


@login_required
def add_product(request,id=0):
    vendor = request.user.vendor
    if request.method == 'GET':
        if id == 0:
            form = ProductForm()
        else:
            product = vendor.products.get(pk=id)
            form = ProductForm(instance=product)
        return render(request, 'vendor/add_product.html', {'form': form})
    else:
        if id == 0:
            form = ProductForm(request.POST,request.FILES)
            messages.success(request, 'Product added succesfully!')
        else:
            product = vendor.products.get(pk=id)
            form = ProductForm(request.POST,request.FILES,instance=product)
            messages.success(request, 'Product modified succesfully!')
    if form.is_valid():
        product = form.save(commit=False)
        product.vendor = request.user.vendor
        product.slug = slugify(product.title)
        product.save()
    return redirect('vendor_admin')


@login_required
def product_delete(request, id):
    vendor = request.user.vendor
    product = vendor.products.get(pk=id)
    product.delete()
    messages.success(request, 'Vendor product successfully deleted!')
    return redirect('vendor_admin')
