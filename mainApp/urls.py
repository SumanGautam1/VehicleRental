from django.urls import path, include
from mainApp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',homepage,name='home'),
    path('about/', about_page, name='about'),

    # dashboards
    path('customer_home/', customer_home, name='customer_home'),
    path('owner_details/', owner_details, name='owner_details'),
    path('admin_home/', admin_home, name='admin_home'),
    
    #dashboard configs
    path('vehicle_on_rent', vehicle_on_rent, name='vehicle_on_rent'),

    # categories
    path('category/', category_all, name='all_category'),
    path('vehicle/<int:pk>', vehicle, name='vehicle'),
    path('individual_category/<str:space>', category_individual, name='individual_category'),
    path('all_vehicles/', all_vehicles, name='all_vehicles'),
    path('vehicle_register/', vehicle_register, name='vehicle_register'),

    # access deny pages
    path('auth_denied/', auth_denied, name='auth_denied'),
    path('customer_needed/', customer_needed, name='customer_needed'),



    # auth section
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('logout/',log_out,name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
