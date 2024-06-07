from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
