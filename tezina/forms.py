from django import forms
from django.contrib.auth.forms import UserCreationForm
from tezina.models import MyUser


class UserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('email','first_name','last_name')

    
       