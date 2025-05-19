from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False,
                                   help_text='Необязательное поле. Введите ваш номер телефона.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'avatar', 'phone_number', 'country')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone_number


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
