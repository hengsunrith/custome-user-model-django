# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout


@login_required
def home(request):
    return render(request, "accounts/home.html", {})


# def dispatch(self, *args, **kwargs):
#     if self.request.user.is_authenticated:
#         return redirect('/')
#     return super.dispatch(*args, **kwargs)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, "accounts/home.html", {})
        else:
            form = LoginForm()
    return render(request, "accounts/login_page.html", {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.profile.birth_date = form.cleaned_data.get("birth_date")
                user.save()
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password1")
                auth = authenticate(request, email=email, password=password)
                if auth is not None:
                    login(request, user)
                    return render(request, "accounts/home.html", {})
        else:
            form = RegisterForm()
    return render(request, "accounts/register.html", {'form': form})


def logout_page(request):
    logout(request)
    return redirect('/')

