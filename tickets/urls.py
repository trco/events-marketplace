from django.urls import path
from tickets import views as tickets_views


urlpatterns = [
    path('tickets/<int:event_id>', tickets_views.manage_tickets,
         name='manage_tickets'),
]
