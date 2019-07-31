from django import forms
from django.contrib.auth import get_user_model

User= get_user_model()


class GuestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Your Email",
        "id": "email"
    }))


class loginForm(forms.Form):
    UserName = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        "id": "username",
        "placeholder":"User name"}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "password",
        "placeholder": "Password"
    }))


class registerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "username",
        "placeholder": "User name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Your Email",
        "id": "email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "password",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "password2",
        "placeholder": "Confirm Password"
    }))

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            print(password)
            print(password2)
            raise forms.ValidationError("password must match.")
        else:
            return data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email2 = User.objects.filter(email=email)
        if email2.exists():
            raise forms.ValidationError("email is already taken.")
        else:
            return email
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is already taken.")
        else:
            return username


