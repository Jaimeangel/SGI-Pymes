from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from rest_framework.authtoken.models import Token
import requests

@login_required(login_url='/login')
def dashboard_home(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login')
def inventory_view(request):
    url = "http://127.0.0.1:8000/api/inventory/stock/"

    # A GET request to the API
    products_inventory = requests.get(url)

    # Print the response
    products_inventory_json = products_inventory.json()
    return render(request, 'inventory.html',{'stock':products_inventory_json})

@login_required(login_url='/login')
def add_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_sale = float(form.cleaned_data['price_sale'])  # Convert Decimal to float
            category = int(form.cleaned_data['category'].id)  # Ensure category is an integer

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'name': name,
                    'description': description,
                    'price_sale': price_sale,
                    'category': category,
                }

                # Define the API endpoint
                api_endpoint = 'http://localhost:8000/api/inventory/products/'

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    return redirect('inventory')
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

