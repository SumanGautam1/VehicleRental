from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Vehicles


USER_TYPE_CHOICES = [
    (0, 'Customer'),
    (1, 'Owner'),
    (2, 'Admin'),
]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    user_type = forms.TypedChoiceField(
        label="Register As",
        choices=USER_TYPE_CHOICES,
        coerce=int,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )



    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']
        if user_type == 2:
            user.is_admin = True
            user.is_owner = False
            user.is_customer = False
        elif user_type == 1:
            user.is_admin = False
            user.is_owner = True
            user.is_customer = False
        else:
            user.is_admin = False
            user.is_owner = False
            user.is_customer = True
        if commit:
            user.save()
        return user


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        fields = ['vehicle_model', 'rent_price', 'category', 'description', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }