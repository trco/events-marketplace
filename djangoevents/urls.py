from django.contrib import admin
from django.urls import include, path
from events import views as events_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/redirection/', events_views.login_redirection,
         name='login_redirection'),
    path('', events_views.index, name='index'),
    path('<str:username>', events_views.user_profile, name='user_profile'),
    path('events/add', events_views.create_update_event, name='create_event'),
    path('events/edit/<int:event_id>', events_views.create_update_event,
         name='update_event')
]
