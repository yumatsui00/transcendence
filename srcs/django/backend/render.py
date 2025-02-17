from django.shortcuts import render, redirect
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

def home_page(request):
	return render(request, "authorized/home.html")

def setting_page(request):
    return render(request, "authorized/setting/setting.html")


@api_view(["GET"])
def matchmaking_page(request):
    return render(request, "authorized/matchmaking.html")

@api_view(["GET"])
def matchgame_page(request, room_name):
    return render(request, "authorized/match-game.html", {'room_name': room_name})
