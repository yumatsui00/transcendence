from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .utils import error_response, success_response
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected page only for logged-in users!"})


def index(request):
    return JsonResponse({"message": "Welcome to the API!"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    JWT access_token からユーザー情報を取得
    """
    # ✅ Django の `request.user` は JWT に基づいてユーザーを取得
    user = request.user

    # ✅ ユーザー情報をレスポンスとして返す
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "language": user.language,
        "color": user.color,
        "is_2fa_enabled": user.is_2fa_enabled,
        "profile_image": user.profile_image.url
    }
    
    return Response(user_data, status=200)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.POST

    print("🔍 受信データ:", data)  # デバッグ用
    print("🔍 受信ファイル:", request.FILES)  # デバッグ用

    password = data.get("password")
    if not user.check_password(password):
        return Response({"error": "Incorrect password"}, status=400)

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.language = data.get("language", user.language)

    if "profile_image" in request.FILES:
        user.profile_image = request.FILES["profile_image"]

    user.save()
    return Response({"message": "Profile updated successfully"}, status=200)

