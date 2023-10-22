# Creating customer order
# 1.Present a user with an order form to fill in their data
# 2.Create a new Order instance with the data entered, and create an associated OrderItem instance
# for each item in the cart
# 3.Clear all the cart’s contents and redirect the user to a success page

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
        
