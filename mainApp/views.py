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
    vehicles = Vehicles.objects.filter(category=category)
    context = {
                 'vehicles':vehicles, 
                 'category':category,
            }
            
    return render(request, 'category/individual_category.html', context)

def all_vehicles(request):
     vehicles = Vehicles.objects.all()

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




# dashboard section start
def profile(request):
     return render(request, 'auth/profile_load.html')

@customer_only
def customer_home(request):
     return render(request, 'pages/customer/customer_home.html')

@owner_only
def owner_home(request):
     return render(request, 'pages/owner/owner_home.html')

@owner_only
def vehicle_register(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('owner_home')
    else:
        form = VehicleForm()
    return render(request, 'pages/owner/vehicle_register.html', {'form': form})

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
                return redirect('owner_home')
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