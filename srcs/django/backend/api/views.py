from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .utils import error_response, success_response
import json
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


@csrf_exempt
def signup_view(request):
	if request.method == "POST":
		try:
			data = json.loads(request.body)
			username = data.get("username")
			email = data.get("email")
			password = data.get("password")
			language = data.get("language")
			color = 0

			if not username or not email or not password or language is None:
				return error_response("All fields are required")
			#username email の重複チェック
			if CustomUser.objects.filter(username=username).exists():
				return error_response("Username already exists")
			if CustomUser.objects.filter(email=email).exists():
				return error_response("Email already exists")
			# passをハッシュ化して保存
			hashed_password = make_password(password)

			#新しいユーザを作成
			user = CustomUser.objects.create(
				username=username,
				email=email,
				password=password,
				language=language,
				color=color
			)

			# jwttokenを発行
			refresh = RefreshToken.for_user(user)
			access_token = str(refresh.access_token)

			#2FAを実行 (Google AuthenticatiorでQR登録)
			device, created = TOTPDevice.objects.get_or_create(user=user, name="default")
			otp_secret = device.key
			qr = qrcode.make(f"otpauth://totp/{username}?secret={otp_secret}")
			buffer = BytesIO()
			qr_base64 = base64.b64encode(buffer.getvalue()).decode()

			return success_response("User created successfully", {
				"access_token": access_token,
				"refresh_token": str(refresh),
				"qr_code": qr_base64  # QR コードをフロントで表示して Google Authenticator でスキャン
			})

		except Exception as e:
			return error_response(str(e), status=500)

	return error_response("Invalid request method", status=405)


