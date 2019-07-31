from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import Contact_Form, loginForm, registerForm, FormRegister

from django.contrib.auth import logout
from django.urls import reverse
User = get_user_model()

def logout_view(request):
    logout(request)
    return index(request)



def index(request):
    #print(images.image1.url)
    if request.method == "POST":
        print(request.POST)
    return render(request, "home.html", {})


def signup(request):
    form = FormRegister(request.POST or None)
    context = {
        "form":form
    }
    return render(request, "signup.html", context)


def contact(request):
    form = Contact_Form(request.POST or None)
    if form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message": "Thanks for contacting us! your record has been saved."})
    if form.errors:
        errors = form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type="application/json")

    context = {
        "form":form,
    }
    return render(request,"contact.html",context)

def login_page(request):
    form = loginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        #form = loginForm(request.POST or None)

        username = form.cleaned_data.get("UserName")
        password = form.cleaned_data.get("Password")
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            print(user)
            return index(request)
    return render(request, "login.html", context)

def register_page(request):
    form = registerForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        password2 = form.cleaned_data.get("password2")
        newUser = User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request,user)
            return index(request)
    return render(request, "register.html", context)