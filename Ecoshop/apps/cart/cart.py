from decimal import Decimal
from django.conf import settings
from apps.product.models import Product
from apps.coupon.models import Cupon


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.cupon_id = self.session.get('cupon_id')
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
               self.remove(product_id)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Product.objects.get(pk=p)
        return sum(Decimal(item['product'].price) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def cupon(self):
        if self.cupon_id:
            return Cupon.objects.get(id=self.cupon_id)
        return None

    def get_discount(self):
        if self.cupon:
            return (self.cupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def get_amount_saved_after_discount(self):
        return self.get_total_price() - self.get_total_price_after_discount()

    def get_total_saved(self):
        return sum(self.cart.keys()* get_amount_saved_after_discount)
