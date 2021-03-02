from django import forms


class addToCartForm(forms.Form):
    quantity = forms.IntegerField()
