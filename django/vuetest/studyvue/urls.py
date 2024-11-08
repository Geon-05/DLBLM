from django.urls import path
from . import views

urlpatterns = [
    path('api/send_message/', views.send_message, name='send_message'),
    path("", views.studyvue, name="studyvue"),
]
