from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import ProductForm
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

@login_required(login_url='/login')
def detail_product(request,pk):
    url = f"http://127.0.0.1:8000/api/inventory/products/{pk}"

    try:
        product_detail = requests.get(url)
        product_detail.raise_for_status() 

        # Print the response
        product_detail_json = product_detail.json()
        return render(request, 'detail_product.html', {'product': product_detail_json})
    
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return HttpResponse("An error occurred.", status=500)
    
    except ValueError as val_err:
        print(f"JSON decoding failed: {val_err}")
        return HttpResponse("Error decoding JSON response.", status=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)

@login_required(login_url='/login')
def delete_product(request,pk):
    url = f"http://127.0.0.1:8000/api/inventory/products/{pk}"

    try:
        product_detail = requests.delete(url)
        product_detail.raise_for_status() 

        return redirect('inventory')
    
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return HttpResponse("An error occurred.", status=500)
    
    except ValueError as val_err:
        print(f"JSON decoding failed: {val_err}")
        return HttpResponse("Error decoding JSON response.", status=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)

@login_required(login_url='/login')
def edit_product(request, pk):
    url = f"http://127.0.0.1:8000/api/inventory/products/{pk}/"

    # Obtener el token del usuario autenticado
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Extract data from form
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_sale = float(form.cleaned_data['price_sale'])
            category = int(form.cleaned_data['category'].id)

            payload = {
                'name': name,
                'description': description,
                'price_sale': price_sale,
                'category': category,
            }

            # Realizar una solicitud PUT a la API para actualizar el producto
            response = requests.put(url, json=payload, headers=headers)
            if response.status_code == 200:
                return redirect('inventory')
            else:
                print('API request failed:', response.text)
        else:
            print('Form is not valid')
    else:
        # Realizar una solicitud GET a la API para obtener los datos actuales del producto
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            product_data = response.json()

            # Inicializar el formulario con los datos actuales del producto
            form = ProductForm(initial={
                'id': product_data['id'],
                'name': product_data['name'],
                'description': product_data['description'],
                'price_sale': product_data['price_sale'],
                'category': product_data['category'],  # Ajusta según el campo de tu formulario
            })
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return HttpResponse("An error occurred.", status=500)
        except ValueError as val_err:
            print(f"JSON decoding failed: {val_err}")
            return HttpResponse("Error decoding JSON response.", status=500)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)

    return render(request, 'edit_product.html', {'form': form,'product': product_data})