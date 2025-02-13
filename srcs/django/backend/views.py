from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .api.utils import *
from .api.models import CustomUser
import pyotp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes  # ✅ 追加
from rest_framework.permissions import IsAuthenticated
import re
import qrcode
import io
import base64
import json
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken 

CustomUser = get_user_model()

def get_user_from_token(request):
    """headerのjwtを取得し、デコードしてユーザーを判定する"""
    auth = JWTAuthentication()
    header = request.headers.get("Authorization")
    if not header:
        return None
    
    try:
        user, _ = auth.authenticate(request)
        return user
    except AuthenticationFailed:
        return None


@api_view(["GET"])
def check_auth(request):
	"""✅ 認証チェック API(ユーザーのIDとEmailをレスポンスに含める)"""
	user = get_user_from_token(request)

	if user is None:
		return error_response("user not found", {"is_authenticated": False, "detail": "Not authenticated"}, status=401)

	return success_response(
		"authentication verified",
		{
		"is_authenticated": True,
		"user": {
			"id": user.id,
			"email": user.email
		}
	})



@csrf_exempt
@api_view(["GET"])
def qr_view(request):
	email = request.GET.get("email")
	qr_code_url = request.GET.get("qr_code_url")

	if not email or not qr_code_url:
		return JsonResponse({"error": "Invalid request"}, status=400)

	# ✅ `qr.html` をレンダリング
	return render(request, "Unauthorized/qr.html", {"qr_code_url": qr_code_url})


@csrf_exempt
@api_view(["POST"])
def signup_view(request):
	username = request.data.get("username")
	email = request.data.get("email")
	password = request.data.get("password")
	language = request.data.get("language")
	color = 0
	profile_image = request.FILES.get("profile_image")

	is_2fa_enabled = str(request.data.get("is_2fa_enabled", False)).lower() in ["true", "1"]

	if not username or not email or not password or language is None:
		return error_response("All fields are required")
	#username email の重複チェック
	if CustomUser.objects.filter(username=username).exists():
		return error_response("Username already exists")
	if CustomUser.objects.filter(email=email).exists():
		return error_response("Email already exists")
	if len(username) > 10:
		return error_response("username too long")

	if not re.match(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+$", email):
		return error_response("Invalid Email")

	# パスワードのバリデーション（大文字・小文字・数字を含む8文字以上）
	password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
	if not password_regex.match(password):
		return error_response("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one number.")

	# passをハッシュ化して保存
	hashed_password = make_password(password)

	otp_secret = pyotp.random_base32() if is_2fa_enabled else "" #2FA用のシークレットキーを作成


	qr_code_url = None
	# 2fa用のqrコード生成
	if is_2fa_enabled:
		#otp_secretはOTPを作成するための秘密鍵のようなもので、これをもとに新しいTOTPを作成。そのURIを作成
		otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=email, issuer_name="トラセン")
		#otp_uriをQRコードに変換
		qr = qrcode.make(otp_uri)
		#qrをPNG形式でメモリに格納→フロントエンドでかんたんに表示
		qr_io = io.BytesIO()
		qr.save(qr_io, format="PNG")

		# QRコードを Base64 でエンコードしてレスポンスに含める
		qr_code_base64 = base64.b64encode(qr_io.getvalue()).decode("utf-8")
		qr_code_url = f"data:image/png;base64,{qr_code_base64}"

	user = CustomUser.objects.create(
		username=username,
		email=email,
		password=hashed_password,
		language=language,
		color=0,
		profile_image=profile_image if profile_image else "profile_images/default.png",
		otp_secret=otp_secret,
		is_2fa_enabled=is_2fa_enabled,
		qr_code_url=qr_code_url,
	)

	return success_response(
		"SignUp successful. Scan QR to enable 2FA" if is_2fa_enabled else "SignUp Successful",
		{
			"is_2fa_enabled": is_2fa_enabled,
			"password": password,
			"email":email,
			"qr_code_url": qr_code_url
		}
	)

@api_view(["GET"])
def otp_view(request):
	email = request.GET.get("email")
	qr_code_url = request.GET.get("qr_code_url")

	if not email or not qr_code_url:
		return JsonResponse({"error": "Invalid request"}, status=400)

	# ✅ `qr.html` をレンダリング
	return render(request, "Unauthorized/otp.html", {"qr_code_url": qr_code_url})



@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    if not email or not otp:
        return Response({"message": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if not user.otp_secret:
        return Response({"message": "2FA is not enabled for this user"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ ワンタイムパスワードの検証
    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(otp, valid_window=1):  # ⬅ 時間ずれを考慮
        # ✅ 2FA認証済みフラグを True に更新
        user.is_2fa_verified = True
        user.temp_login = True
        user.last_login = timezone.now()  # ついでに最終ログインも更新
        user.save(update_fields=["is_2fa_verified", "temp_login", "last_login"])  # 最適化

        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):
	try:
		data = json.loads(request.body)
		email = data.get("email")
		try:
			user = CustomUser.objects.get(email=email)
		except CustomUser.DoesNotExist:
			return error_response("Invalid email or password1")

		if not email:
			return error_response("Email and Password are required")

		if user.temp_login == False:
			password = data.get("password")
			if not password:
				return error_response("Email and Password are required")

			if not check_password(password, user.password):
				return error_response("Invalid email or password2")	

			#ここで2faが行われているか見る
			if user.is_2fa_enabled and not user.is_2fa_verified:
				return success_response("2FA authentication required", {"requires_2fa": True, "email": email, "qr_code_url": user.qr_code_url})

		# ✅ 2回目のログイン（2FA 認証後 or 2FA 無効なユーザー）→ JWT 発行
		user.temp_login = False
		user.save(update_fields=["temp_login"])
		refresh = RefreshToken.for_user(user)
		return success_response("Login Success", {
			"requires_2fa": False,
			"access_token": str(refresh.access_token),
			"refresh_token": str(refresh)
		})

	except json.JSONDecodeError:
		return error_response("Invalid JSON")


@api_view(["POST"])
@permission_classes([IsAuthenticated])  # JWT 認証が必要
def logout_view(request):
    user = request.user

    # 🔹 ユーザーのステータス変更
    user.is_active = False  # ユーザー無効化
    user.is_2fa_verified = False  # 2FA 認証をリセット
    user.save()

    # 🔹 JWT のトークン無効化（Blacklist に追加）
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # トークンを無効化（Blacklist 機能が有効な場合）
    except Exception as e:
        return Response({"error": "Invalid refresh token", "detail": str(e)}, status=400)

    return Response({"message": "User logged out and deactivated"}, status=200)