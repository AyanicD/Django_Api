from django.shortcuts import render
from django.http import HttpResponse

def create_user(request):
    return HttpResponse("user")

def about(request):
    return render(request, 'blog/home.html')