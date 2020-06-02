from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


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
