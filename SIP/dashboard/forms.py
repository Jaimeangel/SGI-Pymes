from stock_product.models import Product
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price_sale']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Nombre del producto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control-product',
                'placeholder': 'Descripción del producto'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control-product'
            }),
            'price_sale': forms.NumberInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Precio de venta'
            }),
        }
