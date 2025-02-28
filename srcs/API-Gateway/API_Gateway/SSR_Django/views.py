from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests
import os
from django.shortcuts import redirect

def is_authorized(request):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return False, None
    headers = {"Authorization": f"Bearer {access_token}"}
    auth_response = requests.get("https://innerproxy/auth/check-jwt/", headers=headers)
    if auth_response.status_code == 200:
        return True, access_token
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return False, None
    refresh_response = request.get("https://innerproxy/auth/refresh/", json={"refresh_token": refresh_token})
    if refresh_response.status_code == 200:
        new_access_token = refresh_response.json().get("access_token")
        return True, new_access_token
    return False, None


def django_render(url):
    ssr_response = requests.get(url)
    return HttpResponse(ssr_response.content, status=ssr_response.status_code)

def landing_page_view(request):
    status, access_token =is_authorized(request)
    if status is False or access_token is None:
        return django_render("https://innerproxy/")
    return redirect("https://yumatsui.42.fr/pages/home/")

def signup_page_view(request):
    status, access_token =is_authorized(request)
    if status is False or access_token is None:
        return django_render("https://innerproxy/signup")
    return redirect("https://yumatsui.42.fr/pages/home/")

def login_page_view(request):
    status, access_token =is_authorized(request)
    if status is False or access_token is None:
        return django_render("https://innerproxy/login")
    return redirect("https://yumatsui.42.fr/pages/home/")

# def auth_render(request, url):
#     access_token = request.COOKIES.get("access_token")
#     if not access_token:
#         return JsonResponse({"error": "Unauthorized"}, status=401)

#     # ✅ API Gateway が `SSR-Django` にリクエストを送る
#     headers = {"Authorization": f"Bearer {access_token}"}
#     ssr_response = requests.get(url, headers=headers)
#     # ✅ `SSR-Django` のレスポンスをそのまま返す
#     return HttpResponse(ssr_response.content, status=ssr_response.status_code)

def home_page(request):
    status, access_token = is_authorized(request)
    if status is False or access_token is None:
        return redirect("https://yumatsui.42.fr")
    return django_render("https://innerproxy/pages/home/")


def setting_page(request):
    status, access_token = is_authorized(request)
    if status is False or access_token is None:
        return redirect("https://yumatsui.42.fr")
    return django_render("https://innerproxy/pages/setting/")

def matchmaking_page(request):
    status, access_token = is_authorized(request)
    if status is False or access_token is None:
        return redirect("https://yumatsui.42.fr")
    return django_render("https://innerproxy/pages/matchmaking/")

def matchgame_page(request, room_name):
    status, access_token = is_authorized(request)
    if status is False or access_token is None:
        return redirect("https://yumatsui.42.fr")
    return django_render(f"https://innerproxy/pages/match-game/{room_name}/")