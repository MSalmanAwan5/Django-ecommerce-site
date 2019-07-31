from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import loginForm, registerForm, GuestForm
from django.utils.http import is_safe_url
from django.contrib.auth import logout
from django.urls import reverse
from .models import GuestEmail


User = get_user_model()

# Create your views here.
def logout_view(request):
    logout(request)
    return index(request)



def index(request):
    #print(images.image1.url)
    if request.method == "POST":
        print(request.POST)
    return render(request, "home.html", {})


def guest_register_view(request):
     form = GuestForm(request.POST or None)
     print(request.POST)
     next_ = request.GET.get('next')
     next_post_ = request.POST.get('next')
     print("next_post:" + next_post_)
     redirect_path = next_ or next_post_ or None
     if form.is_valid():

        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        # return redirect(redirect_path)
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')

#     return redirect('/register/')



def login_page(request):
    form = loginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)

        username = form.cleaned_data.get("UserName")
        password = form.cleaned_data.get("Password")
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            next_ = request.GET.get('next')
            next_post_ = request.POST.get('next')
            redirect_path = next_ or next_post_ or None
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                redirect('/')

            return index(request)
    return render(request, "accounts/login.html", context)

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
    return render(request, "accounts/register.html", context)