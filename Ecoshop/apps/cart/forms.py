#!/usr/bin/python
# - *- coding: utf- 8 - *-

from django import forms

PAYMENT_CHOICES=(
    ('s','Stripe'),
    ('M','M-Pesa'),
    ('P','Paypal')
)

class CheckoutForm(forms.Form):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}),max_length=100)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}),max_length=100)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email e.g youremail@example.com','class':'d-block w-100'}),max_length=255)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Tel e.g +2547000000000'}),max_length=10)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Adress e.g 1234 Main St'}),max_length=255)
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'d-block w-100','placeholder':'Enter city'}),max_length=100)
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'zip code e.g 40100'}),max_length=100)
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)
    stripe_token=forms.CharField(max_length=255)
    same_billing_addres=forms.BooleanField(required=False)
    save_info=forms.BooleanField(required=False)

