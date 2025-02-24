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
    auth_header = request.headers.get("Authorization")
    print(f"Authorization Header: {auth_header}")  
    if not auth_header or not auth_header.startswith("Bearer "):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    access_token = auth_header.split(" ")[1]
    headers = {"Authorization": f"Bearer {access_token}"}

    
    # ✅ Auth に `access_token` を送信し、レスポンスを取得
    auth_response = requests.get("https://innerproxy/auth/check-jwt/", headers=headers, verify=False)

    if auth_response.status_code == 200:
        auth_data = auth_response.json() 
        userid = auth_data.get("userid")
        
        return render(request, "Authorized/home.html", {"userid": userid})

    return JsonResponse({"error": "Unauthorized"}, status=401)
