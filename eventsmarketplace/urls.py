from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('events/search/', include('haystack.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('events.urls')),
    path('', include('tickets.urls')),
]
