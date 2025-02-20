from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .models import CustomUser
import requests
import os
from django.conf import settings


def error_response(message, status=400):
    return JsonResponse({"success": False, "message": message}, status=status)

def success_response(message, data={}):
    return JsonResponse({"success": True, "message": message, **data}, status=200)

def ask_pass_check(password):
    auth_service_url = os.getenv("AUTH_SERVICE_URL", "https://internal-api-gateway/auth")
    pass_check_url = f"{auth_service_url}/password-check/"
    try:
        response = requests.post(pass_check_url, json={"password": password}, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


# authにuserid, passを登録する
def ask_auth_register(data):
    auth_service_url = os.getenv("AUTH_SERVICE_URL", "https://internal-api-gateway/auth")
    auth_register_url = f"{auth_service_url}/register/"
    try:
        auth_response = requests.post(auth_register_url, json=data, timeout=5)
        return auth_response.status_code
    except requests.exceptions.RequestException:
        return None

# 2FAに登録
def ask_2FA_register(data):
    twoFA_serivice_url = os.getenv("2FA_SERVICE_URL", "https://internal-api-gateway/2fa")
    twoFA_register_url = f"{twoFA_serivice_url}/register/"
    try:
        twoFA_response = requests.post(twoFA_register_url, json=data, timeout=5)
        return twoFA_response.status_code
    except requests.exceptions.RequestException:
        return None

#TODO
def is_email_valid(email):
    return True

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    language = request.data.get("language")
    is_2fa_enabled = bool(request.data.get("is_2fa_enabled", False))

    if not username or not email or not password or language is None:
        return error_response("All fields are required")

    if len(username) > 10:
        return error_response("Username too long")
    if not is_email_valid(email):
        return error_response("Inavlid email")

    # username, email の重複チェック
    if CustomUser.objects.filter(username=username).exists():
        return error_response("Username already exists")
    if CustomUser.objects.filter(email=email).exists():
        return error_response("Email already exists")


    # password チェック
    status = ask_pass_check(password)
    if status != 200:
        if status is None:
            error_response("Auth-Service unreachable", status=500)
        return error_response("Invalid Password")


    user = CustomUser.objects.create(username=username, email=email, language=language, color=0)
    # auth-serviceへの登録
    data = {"userid": user.id, "password": password}
    status = ask_auth_register(data)
    if status != 200:
        user.delete()
        if status is None:
            return error_response("Auth-Service unreachable", status=500)
        return error_response("Invalid password when signing up")

    data = {"userid":user.id, "is_2fa_enabled": is_2fa_enabled, "email": email}
    status = ask_2FA_register(data)
    # return error_response("stat", status=status)
    is_2fa_success = True
    if status is None or status != 200:
        is_2fa_success = False

    return success_response("User registered successfully", {
        "userid": user.id,
        "is_2fa_enabled": is_2fa_enabled,
        "is_2fa_success": is_2fa_success,
    })

