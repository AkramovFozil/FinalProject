from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'avatar', 'password1', 'password2']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise forms.ValidationError("Name must be at least 5 characters")
        return name

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if not avatar:
            raise forms.ValidationError("Avatar is required")
        return avatar