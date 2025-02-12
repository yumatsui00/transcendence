from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
def landing_page(request):
	return render(request, "Unauthorized/index.html")

@api_view(["GET"])
def signup_page(request):
	return render(request, "Unauthorized/signup.html")

@api_view(["GET"])
def login_page(request):
	return render(request, "Unauthorized/login.html")

@api_view(["GET"])
def home_page(request):
	return render(request, "authorized/home.html")

@api_view(["GET"])
def setting_page(request):
    return render(request, "authorized/setting/setting.html")

@api_view(["GET"])
def matchmaking_page(request):
    #TODO トークンを持っている→/homeへ
    return render(request, "matchmaking.html")
