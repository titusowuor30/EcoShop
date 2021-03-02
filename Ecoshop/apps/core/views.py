from django.shortcuts import render

from apps.product.models import Product


def frontpage(request):
    newestProducts = Product.objects.all()[0:8]
    return render(request, 'core/home-page.html', {'newestProducts': newestProducts})


def contact(request):
    return render(request, 'core/contact.html')


def category(request, category_slug):
    category = get_
