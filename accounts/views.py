from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


def login_redirection(request):
    return HttpResponseRedirect(reverse(
        'user_profile',
        args=[request.user.username])
    )


def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        return redirect('login')

    return render(request, 'accounts/signup.html')
