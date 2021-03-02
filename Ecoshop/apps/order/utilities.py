from apps.cart.cart import Cart

from .models import Order,OrderItem

def checkout(request,first_name,last_name,email,address,phone,city,postal_code,amount):
    order=Order.objects.create(first_name=first_name,last_name=last_name,
                               email=email,address=address,
                               phone=phone,city=city,
                               postal_code=postal_code,
                               amount=amount)
    for item in Cart(request):
        OrderItem.objects.create(order=order,product=item['product'],vendor=item['product'].vendor,price=item['product'].price,quantity=item['quantity'])
        order.vendors.add(item['product'].vendor)
        return order