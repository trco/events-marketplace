from django.urls import path
from tickets import views as tickets_views


urlpatterns = [
    path('tickets/add/<int:event_id>', tickets_views.create_ticket,
         name='create_ticket')
]
