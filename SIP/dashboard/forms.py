from stock_product.models import Product
from cliente.models import Client
from supplier.models import Supplier
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

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'identity', 'phone_contact','address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Nombre del producto'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Descripción del producto'
            }),
            'identity': forms.NumberInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Numero de indentidad cliente'
            }),
            'phone_contact': forms.NumberInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Celular de contacto'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Dirección del cliente'
            }),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_number', 'identity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control-product',
                'placeholder': 'Nombre del proveedor'
            }),
            'identity': forms.NumberInput(attrs={
                'class': 'form-control-product'
            }),
            'contact_number': forms.NumberInput(attrs={
                'class': 'form-control-product'
            }),
        }