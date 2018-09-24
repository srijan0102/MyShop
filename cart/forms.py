from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Quantity choice between 1 to 5


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)  # convert input into int
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
