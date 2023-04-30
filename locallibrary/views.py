from django.shortcuts import render


def view_404(request, *args, **kwargs):
    context = {}
    return render(request, 'error_404.html', context)


def view_403(request, *args, **kwargs):
    context = {}
    return render(request, 'error_403.html', context)


def view_500(request, *args, **kwargs):
    context = {}
    return render(request, 'error_500.html', context)
