import os

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings

from users.forms import EmailForm


def pre_register(request):

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data.get('email_address')
            register_link = f'{settings.DEFAULT_DOMAIN}{reverse("register")}'
            send_mail(
                'Join LocalLibrary!',
                'Click the link below.',
                os.environ.get('EMAIL_USER1'),
                [email_address, ],
                fail_silently=False,
                html_message=f'Click the link below to register: <br/> <a href="{register_link}">{register_link}</a>'
            )
            messages.success(request,
                             f'An email has been sent to <a class="alert-link">{email_address}</a> !',
                             extra_tags='safe')
            return redirect(reverse('index'))

    else:
        form = EmailForm()

    context = {'form': form}

    return render(request, 'users/email_form.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(
                request, f'Account created for <a class="alert-link ml-1">{username}</a> !',
                extra_tags='safe'
            )
            form.save()
            # Log User In
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect(reverse('index'))
    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'users/register.html', context)


class MyLoginView(SuccessMessageMixin, LoginView):
    success_message = 'Successfully logged-in!'
