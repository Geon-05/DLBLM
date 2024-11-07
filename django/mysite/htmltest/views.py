from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse


def main(request):
    return render(request, "htmltest/main.html")
