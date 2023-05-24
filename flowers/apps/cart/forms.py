from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Кол-во', initial=1,  widget=forms.NumberInput(attrs={'class': 'quantity'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
