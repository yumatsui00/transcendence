from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@permission_classes([AllowAny]) 
def landing_page(request):
    return render(request, "Unauthorized/index.html") 

@permission_classes([AllowAny]) 
def signup_page(request):
    return render(request, "Unauthorized/signup.html")

@permission_classes([AllowAny]) 
def login_page(request):
    return render(request, "Unauthorized/login.html")

