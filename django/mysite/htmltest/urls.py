from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("testpage/", views.testpage, name="testpage"),
]