from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import base64
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def landing_page(request):
    return render(request, "Unauthorized/index.html") 


def signup_page(request):
    return render(request, "Unauthorized/signup.html")


def login_page(request):
    return render(request, "Unauthorized/login.html")


def get_qr_page(request, userid, qr_url):
    decoded_qr_url = base64.b64decode(qr_url).decode('utf-8')  # URLデコード
    return render(request, "Unauthorized/qr.html", {"userid": userid, "qr_url": decoded_qr_url})


@api_view(["GET"])
def home_view(request):
    return render(request, "Authorized/home.html")

@api_view(["GET"])
def setting_view(request):
    return render(request, "Authorized/setting.html")

@api_view(["GET"])
def matchmaking_page(request):
    return render(request, "Authorized/matchmaking.html")

@api_view(["GET"])
def matchgame_page(request, room_name):
    return render(request, "Authorized/match-game.html", {'room_name': room_name})
