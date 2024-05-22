from django.shortcuts import render,redirect
from .models import *
from .forms import SignUpForm, LoginForm, VehicleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import admin_only, owner_only, customer_only
import requests
import json

# Create your views here.
def homepage(request):
    works = Works.objects.all() # for the working process of the system
    context = {
        'works':works,
    }
    return render(request,'pages/homepage.html',context)

def about_page(request):
    return render(request, 'pages/about.html')


def category_all(request):
        category = Category.objects.all()
        context = {
                    'category':category,
                }
                
        return render(request, 'category/categories.html', context)

def category_individual(request,space):
    space = space.replace('-', ' ')
    category = Category.objects.get(name=space)
    vehicles = Vehicles.objects.filter(category=category,isDelete=False)
    context = {
                 'vehicles':vehicles, 
                 'category':category,
            }
            
    return render(request, 'category/individual_category.html', context)

def all_vehicles(request):
     vehicles = Vehicles.objects.filter(isDelete=False)

     context={
          'vehicles':vehicles
     }
     return render(request, 'category/all_vehicles.html', context)

def vehicle(request,pk):
    vehicle = Vehicles.objects.get(id=pk)
    context = {
         'vehicle':vehicle,     
    }

    return render(request, 'pages/vehicle.html',context)

# Check if the input is a non-null and non-empty value
def is_valid_queryparam(param):
    return param != '' and param is not None

# Search vehicle plus filter
def search_vehicle(request):
    qs = Vehicles.objects.filter(isDelete=False)
    # categories = Category.objects.all()
    searched = request.GET.get('searched')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    category = request.GET.get('category')

    if is_valid_queryparam(searched): # for the model name search
        qs = qs.filter(vehicle_model__icontains=searched)

    if is_valid_queryparam(min_rate):   # minimum rental price
        qs = qs.filter(rent_price__gte=min_rate)

    if is_valid_queryparam(max_rate):   # maximum rental price
        qs = qs.filter(rent_price__lte=max_rate)

    if is_valid_queryparam(category) and category != 'Choose...':   # choose vehicle category
        qs = qs.filter(category__name=category)
    
    return render(request, 'category/search_vehicle.html', {'query': qs, 'searched': searched})


# dashboard section start
def profile(request):
     return render(request, 'auth/profile_load.html')

# customer only section
@customer_only
def customer_details(request):
     return render(request, 'pages/customer/customer_details.html')

@customer_only
def rent_page(request, id):
    vehicle = Vehicles.objects.get(id=id)
    context = {
        "vehicle":vehicle,
    }
    return render(request, 'pages/customer/rent_page.html', context)
# customer only section ends

# owner only section
@owner_only
def owner_details(request):
     return render(request, 'pages/owner/owner_details.html')

@owner_only
def vehicle_register(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)  # Do not save to the database yet
            vehicle.uploaded_by = request.user  # Set the uploaded_by field to the current user
            vehicle.save()  # Now save the instance to the database
            return redirect('owner_details')
    else:
        form = VehicleForm()
    return render(request, 'pages/owner/vehicle_register.html', {'form': form})

@owner_only
def vehicle_update(request, id):
    vehicle = Vehicles.objects.get(id=id)  # Retrieve the vehicle instance by primary key

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()  # Save the updated vehicle instance
            return redirect('vehicle_on_rent')
    else:
        form = VehicleForm(instance=vehicle)  # Populate the form with the existing vehicle data

    return render(request, 'pages/owner/vehicle_update.html', {'form': form})


@owner_only
def vehicle_delete(request, id):
    vehicle = Vehicles.objects.get(id=id)  # Retrieve the vehicle instance by primary key
    vehicle.isDelete=True
    vehicle.save()
    return redirect('vehicle_on_rent')


@owner_only
def vehicle_on_rent(request):
    rented_vehicles = Vehicles.objects.filter(uploaded_by=request.user, isDelete=False)
    context={
        'context':'suman',
        'rented_vehicles': rented_vehicles,
    }
    return render(request, 'pages/owner/vehicle_on_rent.html', context)

# owner only section ends

# admin only section
@admin_only
def admin_home(request):
     return render(request, 'pages/admin/admin_home.html')


# admin only section ends

# access denied section
def auth_denied(request):
     return render(request, 'pages/access/auth_denied.html')

def customer_needed(request):
     return render(request, 'pages/access/customer_needed.html')
# access denied section ends

# dashboard section ends



# auth section start
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User Created")
            return redirect('login_view')
        else:
            messages.error(request, "Invalid Form!")
    else:
        form = SignUpForm()
    return render(request,'auth/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if not User.objects.filter(username=username).exists():
                messages.error(request,"Username doesn't exist")

            elif user is not None and user.is_admin:
                login(request, user)
                messages.success(request, "Welcome Admin")
                return redirect('admin_home')
            elif user is not None and user.is_customer:
                login(request, user)
                messages.success(request, "Welcome customer")
                return redirect('customer_details')
            elif user is not None and user.is_owner:
                login(request, user)
                messages.success(request, "Welcome owner")
                return redirect('owner_details')
            else:
                messages.error(request,"Try again!")
                return redirect('login_view')
        else:
            messages.error(request,"Try again!")
    return render(request, 'auth/login.html', {'form': form, 'msg': msg})

@login_required(login_url='login_view')
def change_password(request):
    cf = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        cf = PasswordChangeForm(user=request.user, data=request.POST)
        if cf.is_valid():   #for validation
            cf.save()
            return redirect('login_view')
    return render(request,'auth/change_password.html',{'cf':cf})

def log_out(request):
    logout(request)
    return redirect('login_view')

# auth section end




# Payment section begin

def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    website_url = request.POST.get('return_url')
    amount = 1000
    purchase_order_id = request.POST.get('purchase_order_id')
    purchase_order_name = request.POST.get('purchase_order_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')


    print("url",url)
    print("return_url",return_url)
    print("web_url",website_url)
    print("amount",amount)
    print("purchase_order_id",purchase_order_id)
    print('username',username)
    print('email',email)
    print('phone',phone)
    payload = json.dumps({
        "return_url": return_url,
        "website_url": return_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": purchase_order_name,
        "customer_info": {
            "name": username,
            "email": email,
            "phone": phone,
        }
    })

    # put your own live secet for admin
    headers = {
        'Authorization': 'Key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res = json.loads(response.text)

    print(type(new_res))
    # return redirect('notices')
    # print(response.json())
    # print(new_res['payment_url'])
    return redirect(new_res['payment_url'])