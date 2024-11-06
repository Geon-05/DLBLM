from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("""
Hello, world. You're at the polls index.<br>
한글 적용
""")
