from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from .forms import ProductForm,ClienteForm,ProveedorForm,OrderPurchaseForm,OrderPurchaseDetailForm,OrderSaleForm,OrderSaleDetailForm
import requests
from django.urls import reverse

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

#Vistas Cliente

@login_required(login_url='/login')
def clientes_view(request):
    url = "http://localhost:8000/api/clients/"

    # A GET request to the API
    clientes = requests.get(url)

    # Print the response
    clientes_json = clientes.json()
    return render(request, 'clients_list.html',{'clientes':clientes_json})

@login_required(login_url='/login')
def add_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            identity = int(form.cleaned_data['identity'])  # Convert Decimal to float
            phone_contact = int(form.cleaned_data['phone_contact'])  # Ensure category is an integer
            address = form.cleaned_data['address']

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'identity': identity,
                    'phone_contact': phone_contact,
                    'address':address
                }

                # Define the API endpoint
                api_endpoint = "http://localhost:8000/api/clients/"

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    return redirect('clients')
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = ClienteForm()

    return render(request, 'add_client.html', {'form': form})

@login_required(login_url='/login')
def detail_cliente(request,pk):
    url = f"http://localhost:8000/api/clients/{pk}"

    try:
        client_detail = requests.get(url)
        client_detail.raise_for_status() 

        # Print the response
        client_detail_json = client_detail.json()
        return render(request, 'detail_client.html', {'client': client_detail_json})
    
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
def delete_cliente(request,pk):
    url = f"http://127.0.0.1:8000/api/clients/{pk}"

    try:
        cliente_detail = requests.delete(url)
        cliente_detail.raise_for_status() 
        print('aqui ocurre esto',cliente_detail)

        return redirect('clients')
    
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
def edit_cliente(request, pk):
    url = f"http://127.0.0.1:8000/api/clients/{pk}/"

    # Obtener el token del usuario autenticado
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Extract data from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            identity = int(form.cleaned_data['identity'])  # Convert Decimal to float
            phone_contact = int(form.cleaned_data['phone_contact'])  # Ensure category is an integer
            address = form.cleaned_data['address']

            payload = {
                'first_name': first_name,
                'last_name': last_name,
                'identity': identity,
                'phone_contact': phone_contact,
                'address':address
            }

            # Realizar una solicitud PUT a la API para actualizar el producto
            response = requests.put(url, json=payload, headers=headers)
            if response.status_code == 200:
                return redirect('clients')
            else:
                print('API request failed:', response.text)
        else:
            print('Form is not valid')
    else:
        # Realizar una solicitud GET a la API para obtener los datos actuales del producto
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            client_data = response.json()

            # Inicializar el formulario con los datos actuales del producto
            form = ClienteForm(initial={
                'id': client_data['id'],
                'first_name': client_data['first_name'],
                'last_name': client_data['last_name'],
                'identity': client_data['identity'],
                'phone_contact': client_data['phone_contact'],  # Ajusta según el campo de tu formulario
                'address': client_data['address'],
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

    return render(request, 'edit_client.html', {'form': form,'cliente': client_data})


#Vistas Proveedores

@login_required(login_url='/login')
def proveedores_view(request):
    url = "http://localhost:8000/api/suppliers/"

    # A GET request to the API
    data = requests.get(url)

    # Print the response
    data_json = data.json()
    return render(request, 'proveedores_list.html',{'proveedores':data_json})

@login_required(login_url='/login')
def add_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            name = form.cleaned_data['name']
            contact_number = int(form.cleaned_data['contact_number'])  # Convert Decimal to float
            identity = int(form.cleaned_data['identity'])  # Ensure category is an integer

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'name': name,
                    'contact_number': contact_number,
                    'identity': identity,
                }

                # Define the API endpoint
                api_endpoint = "http://localhost:8000/api/suppliers/"

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    return redirect('suppliers')
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = ProveedorForm()

    return render(request, 'add_proveedor.html', {'form': form})

@login_required(login_url='/login')
def detail_proveedor(request,pk):
    url = f"http://localhost:8000/api/suppliers/{pk}/"
    

    try:
        proveedor_detail = requests.get(url)
        proveedor_detail.raise_for_status() 

        # Print the response
        proveedor_detail_json = proveedor_detail.json()
        return render(request, 'detail_proveedor.html', {'proveedor': proveedor_detail_json})
    
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
def delete_proveedor(request,pk):
    url = f"http://localhost:8000/api/suppliers/{pk}/"

    try:
        proveedor_detail = requests.delete(url)
        proveedor_detail.raise_for_status() 

        return redirect('suppliers')
    
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
def edit_proveedor(request, pk):
    url = f"http://localhost:8000/api/suppliers/{pk}/"

    # Obtener el token del usuario autenticado
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }

    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            contact_number = int(form.cleaned_data['contact_number'])  # Convert Decimal to float
            identity = int(form.cleaned_data['identity'])  # Ensure category is an integer

            payload = {
                'name': name,
                'contact_number': contact_number,
                'identity': identity,
            }

            # Realizar una solicitud PUT a la API para actualizar el producto
            response = requests.put(url, json=payload, headers=headers)
            if response.status_code == 200:
                return redirect('suppliers')
            else:
                print('API request failed:', response.text)
        else:
            print('Form is not valid')
    else:
        # Realizar una solicitud GET a la API para obtener los datos actuales del producto
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            client_data = response.json()

            # Inicializar el formulario con los datos actuales del producto
            form = ProveedorForm(initial={
                'name': client_data['name'],
                'contact_number': client_data['contact_number'],  # Ajusta según el campo de tu formulario
                'identity': client_data['identity'],
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

    return render(request, 'edit_proveedor.html', {'form': form,'proveedor': client_data})

#ordenes de compra
@login_required(login_url='/login')
def orders_purchase_view(request):
    url = "http://localhost:8000/api/order-purchase/purchase/"

    # A GET request to the API
    data = requests.get(url)

    # Print the response
    data_json = data.json()
    return render(request, 'purchase_list.html',{'orders':data_json})

@login_required(login_url='/login')
def add_order_purchase(request):
    if request.method == 'POST':
        form = OrderPurchaseForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            supplier = int(form.cleaned_data['supplier'].id)

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'supplier': supplier,
                }

                # Define the API endpoint
                api_endpoint = "http://localhost:8000/api/order-purchase/purchase/"

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    return redirect('purchases')
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = OrderPurchaseForm()

    return render(request, 'add_order_purchase.html', {'form': form})

@login_required(login_url='/login')
def detail_order_purchase(request,pk):
    url = f"http://localhost:8000/api/order-purchase/purchase/{pk}/"
    url_detail = f"http://localhost:8000/api/order-purchase/purchase/{pk}/order_details/"
    

    try:
        purchase_detail = requests.get(url)
        purchase_detail.raise_for_status() 

        # Print the response
        purchase_detail_json = purchase_detail.json()
        try:
            order_purchase_detail = requests.get(url_detail)
            order_purchase_detail.raise_for_status() 

            # Print the response
            order_purchase_detail_json = order_purchase_detail.json()

            return render(request, 'detail_order_purchase.html', {'purchase': purchase_detail_json,'purchase_detail':order_purchase_detail_json})

        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return HttpResponse("An error occurred.", status=500)
    
        except ValueError as val_err:
            print(f"JSON decoding failed: {val_err}")
            return HttpResponse("Error decoding JSON response.", status=500)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)
    
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
def delete_order_purchase(request,pk):
    url = f"http://localhost:8000/api/order-purchase/purchase/{pk}/"

    try:
        purchase_detail = requests.delete(url)
        purchase_detail.raise_for_status() 

        return redirect('purchases')
    
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
def add_order_detail_purchase(request,pk):
    if request.method == 'POST':
        form = OrderPurchaseDetailForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            order_supplier = int(pk)
            product = int(form.cleaned_data['product'].id)
            quantity = int(form.cleaned_data['quantity'])
            purchase_price = float(form.cleaned_data['purchase_price'])

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'order_supplier':order_supplier,
                    'product': product,
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                }

                # Define the API endpoint
                api_endpoint = "http://localhost:8000/api/order-purchase/purchase-detail/"

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    # url = reverse('purchases')
                    # print(f'Redirecting to: {url}')
                    return redirect('detail-order-purchase',pk=pk)
                
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = OrderPurchaseDetailForm()
        

    return render(request, 'add_order_detail_purchase.html', {'form': form,'id_order':pk})

@login_required(login_url='/login')
def edit_order_detail_purchase(request,pk,pk_order):
    url = f"http://localhost:8000/api/order-purchase/purchase-detail/{pk}/"

    # Obtener el token del usuario autenticado
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }

    if request.method == 'POST':
        form = OrderPurchaseDetailForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            order_supplier = int(pk_order)
            product = int(form.cleaned_data['product'].id)
            quantity = int(form.cleaned_data['quantity'])
            purchase_price = float(form.cleaned_data['purchase_price'])

            payload = {
                'order_supplier':order_supplier,
                'product': product,
                'quantity': quantity,
                'purchase_price': purchase_price,
            }

            # Realizar una solicitud PUT a la API para actualizar el producto
            response = requests.put(url, json=payload, headers=headers)
            if response.status_code == 200:
                return redirect('detail-order-purchase',pk=pk_order)
            else:
                print('API request failed:', response.text)
        else:
            print('Form is not valid')
    else:
        # Realizar una solicitud GET a la API para obtener los datos actuales del producto
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            client_data = response.json()

            # Inicializar el formulario con los datos actuales del producto
            form = OrderPurchaseDetailForm(initial={
                'product': client_data['product']['id'],
                'quantity': client_data['quantity'],  
                'purchase_price': float(client_data['purchase_price'])
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

    return render(request, 'edit_order_detail_purchase.html', {'form': form,'id_order': client_data['order_supplier']})

@login_required(login_url='/login')
def delete_order_detail_purchase(request,pk,pk_order):
    url = f"http://localhost:8000/api/order-purchase/purchase-detail/{pk}/"

    try:
        purchase_detail = requests.delete(url)
        purchase_detail.raise_for_status() 

        return redirect('detail-order-purchase',pk=pk_order)
    
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
def complete_order_purchase(request,pk):
    url=f"http://127.0.0.1:8000/api/order-purchase/purchase/{pk}/complete_order_purchase/"

    try:
        purchase_detail = requests.post(url)
        purchase_detail.raise_for_status() 

        return redirect('detail-order-purchase',pk=pk)
    
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return HttpResponse("An error occurred.", status=500)
    
    except ValueError as val_err:
        print(f"JSON decoding failed: {val_err}")
        return HttpResponse("Error decoding JSON response.", status=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)


#ordenes de venta
@login_required(login_url='/login')
def orders_sale_view(request):
    url = "http://localhost:8000/api/order-sale/sale/"

    # A GET request to the API
    data = requests.get(url)

    # Print the response
    data_json = data.json()
    return render(request, 'sales_list.html',{'orders':data_json})

@login_required(login_url='/login')
def add_order_sale(request):
    if request.method == 'POST':
        form = OrderSaleForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            client = int(form.cleaned_data['client'].id)

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'client': client,
                }

                # Define the API endpoint
                api_endpoint = "http://localhost:8000/api/order-sale/sale/"

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    return redirect('sales')
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = OrderSaleForm()

    return render(request, 'add_order_sale.html', {'form': form})

@login_required(login_url='/login')
def detail_order_sale(request,pk):
    url = f"http://localhost:8000/api/order-sale/sale/{pk}/"
    url_detail = f"http://localhost:8000/api/order-sale/sale/{pk}/order_details/"
    

    try:
        sale_detail = requests.get(url)
        sale_detail.raise_for_status() 

        # Print the response
        sale_detail_json = sale_detail.json()
        try:
            order_sale_detail = requests.get(url_detail)
            order_sale_detail.raise_for_status() 

            # Print the response
            order_sale_detail_json = order_sale_detail.json()

            return render(request, 'detail_order_sale.html', {'sale': sale_detail_json,'sale_detail':order_sale_detail_json})

        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return HttpResponse("An error occurred.", status=500)
    
        except ValueError as val_err:
            print(f"JSON decoding failed: {val_err}")
            return HttpResponse("Error decoding JSON response.", status=500)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)
    
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
def delete_order_sale(request,pk):
    url = f"http://localhost:8000/api/order-sale/sale/{pk}/"

    try:
        sale_detail = requests.delete(url)
        sale_detail.raise_for_status() 

        return redirect('sales')
    
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
def add_order_detail_sale(request,pk):
    if request.method == 'POST':
        form = OrderSaleDetailForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            order_sale = int(pk)
            product = int(form.cleaned_data['product'].id)
            quantity = int(form.cleaned_data['quantity'])
            sale_price = float(form.cleaned_data['sale_price'])

            # Ensure the user is authenticated
            if request.user.is_authenticated:
                # Get the token of the authenticated user
                token, created = Token.objects.get_or_create(user=request.user)

                # Prepare the payload for the API request
                payload = {
                    'order_sale':order_sale,
                    'product': product,
                    'quantity': quantity,
                    'sale_price': sale_price,
                }

                # Define the API endpoint
                api_endpoint = "http://localhost:8000/api/order-sale/sale-details/"

                # Set up the headers, including the token for authorization
                headers = {
                    'Authorization': f'Token {token.key}',
                    'Content-Type': 'application/json'
                }

                # Make the API request
                response = requests.post(api_endpoint, json=payload, headers=headers)

                # Check if the request was successful
                if response.status_code == 201:
                    # url = reverse('purchases')
                    # print(f'Redirecting to: {url}')
                    return redirect('detail-order-sale',pk=pk)
                
                else:
                    print('API request failed:', response.text)
            else:
                print('User is not authenticated')
                return redirect('login')  # Redirect to login if user is not authenticated
        else:
            print('Form is not valid')
    else:
        form = OrderSaleDetailForm()
        

    return render(request, 'add_order_detail_sale.html', {'form': form,'id_order':pk})

@login_required(login_url='/login')
def edit_order_detail_sale(request,pk,pk_order):
    url = f"http://localhost:8000/api/order-sale/sale-details/{pk}/"

    # Obtener el token del usuario autenticado
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json'
    }

    if request.method == 'POST':
        form = OrderSaleDetailForm(request.POST)
        if form.is_valid():
            # Extract data from form and convert to appropriate types
            order_sale = int(pk_order)
            product = int(form.cleaned_data['product'].id)
            quantity = int(form.cleaned_data['quantity'])
            sale_price = float(form.cleaned_data['sale_price'])

            payload = {
                'order_sale':order_sale,
                'product': product,
                'quantity': quantity,
                'sale_price': sale_price,
            }

            # Realizar una solicitud PUT a la API para actualizar el producto
            response = requests.put(url, json=payload, headers=headers)
            if response.status_code == 200:
                return redirect('detail-order-sale',pk=pk_order)
            else:
                print('API request failed:', response.text)
        else:
            print('Form is not valid')
    else:
        # Realizar una solicitud GET a la API para obtener los datos actuales del producto
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            client_data = response.json()

            # Inicializar el formulario con los datos actuales del producto
            form = OrderSaleDetailForm(initial={
                'product': client_data['product']['id'],
                'quantity': client_data['quantity'],  
                'sale_price': float(client_data['sale_price'])
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

    return render(request, 'edit_order_detail_sale.html', {'form': form,'id_order': client_data['order_sale']})

@login_required(login_url='/login')
def delete_order_detail_sale(request,pk,pk_order):
    url = f"http://localhost:8000/api/order-sale/sale-details/{pk}/"

    try:
        sale_detail = requests.delete(url)
        sale_detail.raise_for_status() 

        return redirect('detail-order-sale',pk=pk_order)
    
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
def complete_order_sale(request,pk):
    url=f"http://localhost:8000/api/order-sale/sale/{pk}/complete_order_sale/"

    try:
        purchase_detail = requests.post(url)
        purchase_detail.raise_for_status() 

        return redirect('detail-order-sale',pk=pk)
    
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return HttpResponse("An error occurred.", status=500)
    
    except ValueError as val_err:
        print(f"JSON decoding failed: {val_err}")
        return HttpResponse("Error decoding JSON response.", status=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)
    

# informes
@login_required(login_url='/login')
def informes_view(request):
    return render(request, 'dashboard_informes.html')

@login_required(login_url='/login')
def dashboard_products_sales(request):
    url = "http://127.0.0.1:8000/api/inventory/stock/"

    # A GET request to the API
    products_inventory = requests.get(url)

    # Print the response
    products_inventory_json = products_inventory.json()
    return render(request, 'dashboard_informes_products_sales.html',{'stock':products_inventory_json})

@login_required(login_url='/login')
def dashboard_products_purchase(request):
    url = "http://127.0.0.1:8000/api/inventory/stock/"

    # A GET request to the API
    products_inventory = requests.get(url)

    # Print the response
    products_inventory_json = products_inventory.json()
    return render(request, 'dashboard_informes_products_purchase.html',{'stock':products_inventory_json})

@login_required(login_url='/login')
def dashboard_products_sales_registry_detail(request,pk):
    url = "http://127.0.0.1:8000/api/inventory/stock/"

    # A GET request to the API
    products_inventory = requests.get(url)

    # Print the response
    products_inventory_json = products_inventory.json()
    return render(request, 'dashboard_informes_products_sales.html',{'stock':products_inventory_json})
