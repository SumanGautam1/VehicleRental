from django.urls import path, include
from mainApp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',homepage,name='home'),
    path('about/', about_page, name='about'),


    path('customer_home/', customer_home, name='customer_home'),
    path('owner_home/', owner_home, name='owner_home'),
    path('admin_home/', admin_home, name='admin_home'),
    
    path('category/', category_all, name='all_category'),
    path('vehicle/<int:pk>', vehicle, name='vehicle'),
    path('individual_category/<str:space>', category_individual, name='individual_category'),
    path('all_vehicles/', all_vehicles, name='all_vehicles'),

    path('signin_option/', profile, name='signin_option'),
    path('access_denied/', access_denied, name='access_denied'),

    # auth section
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('logout/',log_out,name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
