from django.urls import path
from accounts.views import login_redirection, signup

urlpatterns = [
    path('login/redirection/', login_redirection, name='login_redirection'),
    path('signup/', signup, name='signup')
]
