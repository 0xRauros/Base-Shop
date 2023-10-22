from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                    choices=PRODUCT_QUANTITY_CHOICES,
                    coerce=int)
    # If the quantity has to added or overriden.
    # It is hidden since we don't want to display it to the user.
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    
