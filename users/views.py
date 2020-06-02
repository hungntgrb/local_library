from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for <a class="alert-link ml-2">{username}</a>!',
                extra_tags='safe'
            )
            form.save()
            return redirect(reverse('index'))
    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'users/register.html', context)
