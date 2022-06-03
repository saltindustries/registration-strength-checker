from django.conf import settings
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import CreateUserForm

# Login Page
def loginAccountPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            response_recaptcha_handler = request.POST.get('g-recaptcha-response')
            recaptcha_data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': response_recaptcha_handler
            }
            recaptcha_verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_data)
            result = recaptcha_verify.json()
            if result['success']:
                user = authenticate(request, username=username, password=password)
                if user is not None:              
                        login(request, user)
                        return redirect('home')                
                else:
                    messages.info(request, 'Username or password is incorrect.')
            else:
                messages.error(request, 'reCAPTCHA failed. Please verify captcha before logging in.')
            
        context = {}
        return render(request, 'accounts/login.html', context)

# Register Page
def registerAccountPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            response_recaptcha_handler = request.POST.get('g-recaptcha-response')
            recaptcha_data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': response_recaptcha_handler
            }
            recaptcha_verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data = recaptcha_data)
            result = recaptcha_verify.json()
            if result['success']:
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account created with username ' + user)
                    return redirect('login')
            else:
                messages.error(request, 'reCAPTCHA failed. Please verify captcha before registering.')
                
        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/dashboard.html')
