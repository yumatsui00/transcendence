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
        "is_2fa_enabled": user.is_2fa_enabled
    }
    
    return Response(user_data, status=200)



