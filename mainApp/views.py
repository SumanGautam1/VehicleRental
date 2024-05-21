from django.shortcuts import render,redirect
from .models import *
from .forms import SignUpForm, LoginForm, VehicleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import admin_only, owner_only, customer_only

# Create your views here.
def homepage(request):
    works = Works.objects.all()
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

# Search vehicle
def search_vehicle(request):
    qs = Vehicles.objects.filter(isDelete=False)
    # categories = Category.objects.all()
    searched = request.GET.get('searched')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    category = request.GET.get('category')

    if is_valid_queryparam(searched):
        qs = qs.filter(vehicle_model__icontains=searched)

    if is_valid_queryparam(min_rate):
        qs = qs.filter(rent_price__gte=min_rate)

    if is_valid_queryparam(max_rate):
        qs = qs.filter(rent_price__lte=max_rate)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(category__name=category)
    
    return render(request, 'category/search_vehicle.html', {'query': qs, 'searched': searched})


# dashboard section start
def profile(request):
     return render(request, 'auth/profile_load.html')

@customer_only
def customer_home(request):
     return render(request, 'pages/customer/customer_home.html')

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




@admin_only
def admin_home(request):
     return render(request, 'pages/admin/admin_home.html')

def auth_denied(request):
     return render(request, 'pages/access/auth_denied.html')

def customer_needed(request):
     return render(request, 'pages/access/customer_needed.html')
# dashboard section end

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
                return redirect('customer_home')
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