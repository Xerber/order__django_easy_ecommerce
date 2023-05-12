from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User



class UserRegisterForm(UserCreationForm):
  username = forms.CharField(widget=forms.TextInput())
  email = forms.CharField(widget=forms.EmailInput())
  password1 = forms.CharField(widget=forms.PasswordInput())
  password2 = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ['username', 'email']


class UserAuthForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ['username', 'password']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
  

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']