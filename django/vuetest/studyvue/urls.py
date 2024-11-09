from django.urls import path
from . import views

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('send_subject/', views.send_subject, name='send_subject'),
    path("", views.studyvue, name="studyvue"),
]
