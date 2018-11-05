from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        return redirect('login')

    return render(request, 'accounts/signup.html')
