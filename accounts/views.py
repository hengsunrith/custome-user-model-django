# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from Posts.models import Post
from django.utils import timezone

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
def home(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "Posts/post_list.html", {'posts':posts})


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
                    return redirect('/')
        else:
            form = LoginForm()
    return render(request, "accounts/login_page.html", {'form': form})


def register(request):
    # REGISTER USER WITHOUT SENDING MAIL
    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
    #     if request.method == 'POST':
    #         form = RegisterForm(request.POST)
    #         if form.is_valid():
    #             user = form.save()
    #             user.refresh_from_db()  # load the profile instance created by the signal
    #             user.profile.birth_date = form.cleaned_data.get("birth_date")
    #             user.save()
    #             email = form.cleaned_data.get("email")
    #             password = form.cleaned_data.get("password1")
    #             auth = authenticate(request, email=email, password=password)
    #             if auth is not None:
    #                 login(request, user)
    #                 return render(request, "accounts/home.html", {})
    #     else:
    #         form = RegisterForm()
    # return render(request, "accounts/register.html", {'form': form})

    #  REGISTER USER WITH ACTIVATE SENDING MAIL LOCAL
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your Account'
                message = render_to_string('accounts/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(subject, message, 'from@example.com', [user.email], fail_silently=False,)
                return redirect('account_activation_sent')
        else:
            form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


def logout_page(request):
    logout(request)
    return redirect('/')