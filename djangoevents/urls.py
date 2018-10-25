from django.contrib import admin
from django.urls import path
from events import views as events_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', events_views.index, name='index')
]
