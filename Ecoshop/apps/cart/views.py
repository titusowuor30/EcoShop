from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.db.models import ObjectDoesNotExist


from apps.coupon.forms import CuponApllyForm
from apps.order.utilities import checkout
from .forms import CheckoutForm
from .cart import Cart
from apps.order.models import Order, BillingAdress

import stripe


def cart_detail(request):
    cart = Cart(request)
    if request.method == 'POST':
        try:
            order = Order.objects.get(vendor=request.user.vendor)
            form = CheckoutForm(request.POST)
            if form.is_valid():
                stripe.api_key = settings.STRIPE_SECRET_KEY
                stripe_token = form.cleaned_data['stripe_token']
                charge = stripe.Charge.create(
                amount=int(cart.get_total_price() * 100),
                currency='USD',
                description='Charge from Ecohub Electronics',
                    source=stripe_token)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                city = form.cleaned_data['city']
                postal_code = form.cleaned_data['postal_code']
                same_billing_addres = form.cleaned_data['same_billing_addres']
                save_info = form.cleaned_data['save_info']
                billing_addres = BillingAdress(
                user=request.user,
                email=email,
                address=address,
                city=city,
                postal_code=postal_code)
                billing_addres.save()
                order = checkout(request, first_name, last_name, email, phone, address, city, postal_code,
                             cart.get_total_price)
                order.billing_addres = billing_addres
                order.save()
                print(form.cleaned_data)
                cart.clear()
                return redirect('success')
            messages.info(request, 'Your do not have any active orders')
        except ObjectDoesNotExist:
            messages.warning(request, 'Checkout Failed')
        return redirect('cart')
    else:
        form = CheckoutForm()

    cupon_apply_form = CuponApllyForm()

    return render(request, 'cart/checkout-page.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})


def show_cart(request):
    cart = Cart(request)

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        messages.info(request, 'Product removed from cart')
        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, update_quantity=True)
        messages.info(request, 'Product quantity updated')
        return redirect('cart')

    return render(request, 'cart/cart.html')


def success(request):
    return render(request, 'cart/success.html')
