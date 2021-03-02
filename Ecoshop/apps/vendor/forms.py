from django import forms

from apps.product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'additional_info', 'price','image','thumbnail')
        labels = {
            'image': 'Image',
            'thumbnail':'ThumbNail',
        }