from django.shortcuts import render, redirect
from django.contrib import messages, auth
from . forms import UserForm
from .models import User
# from django.contrib.auth import authenticate


def signup(request):
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in.")
    return redirect('accounts:profile')
  elif request.method=='POST':
    form = UserForm(request.POST)
    if form.is_valid():
      password = form.cleaned_data['password']
      user = form.save(commit=False)
      user.set_password(password)
      user.role = User.CUSTOMER
      user.save()
      messages.success(request, "Account Created Successfully")
      return redirect('accounts:login')
    else:
      print(form.errors)
  else:
    form = UserForm()

  context = {'form' : form}

  return render(request, 'accounts/signup.html', context)


def login(request):
  if request.user.is_authenticated:
    messages.warning(request, 'You are already logged in')
    return redirect('accounts:profile')
  elif request.method=='POST':
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(request, email=email, password=password)
    print(user)
    
    if user is not None:
      print(user)
      auth.login(request, user)
      # messages.success(request, 'Login Successfull')
      return redirect('accounts:profile')
    else:
      print('wtf is the user')
      messages.error(request, 'Invalid Credentials')
      return redirect('accounts:login')

  return render(request, 'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request, 'You have logged out')
  return redirect('accounts:login')

def profile(request):
  return render(request, 'accounts/profile.html')
  