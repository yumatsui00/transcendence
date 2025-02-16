from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .api.utils import *
from .api.models import CustomUser, RefreshTokenStore
import pyotp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes  # ✅ 追加
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from ipware import get_client_ip
from datetime import timedelta
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken



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
@permission_classes([IsAuthenticated])
def check_auth(request):
	return Response({"is_authenticated": True}, status=200)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
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
		is_registered_once=False,
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



@csrf_exempt
@permission_classes([AllowAny])
def qr_view(request):
    email = request.GET.get("email")

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    try:
        # ✅ email からユーザーを取得
        user = CustomUser.objects.get(email=email)
        
        # ✅ `qr_code_url` を取得
        if not user.qr_code_url:
            return JsonResponse({"error": "QR code not found"}, status=404)
        if user.is_registered_once:
            return render(request, "Unauthorized/otp.html", {"is_registered_once": True})
        # ✅ `qr.html` をレンダリング
        return render(request, "Unauthorized/qr.html", {"qr_code_url": user.qr_code_url})

    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@api_view(["GET"])
@permission_classes([AllowAny])
def otp_view(request):
    email = request.GET.get("email")

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    try:
        # ✅ email からユーザーを取得
        user = CustomUser.objects.get(email=email)
        # ✅ `qr_code_url` を取得
        if not user.qr_code_url:
            return JsonResponse({"error": "QR code not found"}, status=404)
        if user.is_registered_once:
            return render(request, "Unauthorized/otp.html", {"is_registered_once": True})
        return render(request, "Unauthorized/otp.html", {"qr_code_url": user.qr_code_url, "is_registered_once": False})
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)




@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    device_name = request.data.get("device")  # クライアントからデバイス名を送信
    ip_address = get_client_ip(request)  # クライアントの IP を取得

    if not email or not otp or device_name:
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
        user.last_login = timezone.now()  # ついでに最終ログインも更新
        user.is_registered_once = True
        user.save(update_fields=["last_login", "is_registered_once"])  # 最適化

        # refreshtokenの発行
        # ✅ 新しい `refresh_token` を発行
        refresh = RefreshToken.for_user(user)

        # ✅ `refresh_token` をデータベースに保存
        RefreshTokenStore.objects.create(
            user=user,
            refresh_token=str(refresh),
            expires_at=timezone.now() + timedelta(days=7),  # `SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']` に合わせる
            device_name=device_name,  # クライアントのデバイス情報
            ip_address=ip_address,  # クライアントのIP
        )

        return success_response("OTP verified successfully", {
			"access_token": str(refresh.access_token),
			"refresh_token": str(refresh)
		})
    else:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
	try:
		data = json.loads(request.body)
		email = data.get("email")
		password = data.get("password")
		try:
			user = CustomUser.objects.get(email=email)
		except CustomUser.DoesNotExist:
			return error_response("Invalid email or password1")
		is_2fa_enabled = user.is_2fa_enabled

		if not email:
			return error_response("Email and Password are required")
		if not password:
			return error_response("Email and Password are required")
		if not check_password(password, user.password):
			return error_response("Invalid email or password2")	

		#2fa認証が不要なユーザー
		if not is_2fa_enabled:
			refresh = RefreshToken.for_user(user)
			return success_response("Login Success", {
				"requires_2fa": False,
				"access_token": str(refresh.access_token),
				"refresh_token": str(refresh)
			})


		# クライアントのIP, DEVICEを取得
		ip_address = get_client_ip(request)
		device_name = request.data.get("device")
		# ✅ 既存の `refresh_token` を取得
		valid_token = RefreshTokenStore.objects.filter(
            user=user, 
            expires_at__gt=timezone.now(), 
            ip_address=ip_address, 
            device_name=device_name
        ).first()

		if valid_token:
			print("信用されたデバイスとIPアドレス。2FA認証をスキップします")
			refresh = valid_token.refresh_token
			return success_response("Login Success", {
				"requires_2fa": False,
				"access_token": str(refresh.access_token),
				"refresh_token": refresh
			})
		print("⚠2FA認証が必要です。")
		return success_response("Need to verify 2FA", {
			"requires_2fa": True,
			"email": email,
			"is_registered_once": user.is_registered_once
		})

	except json.JSONDecodeError:
		return error_response("Invalid JSON")


@api_view(["POST"])
@permission_classes([IsAuthenticated])  # JWT 認証が必要
def logout_view(request):
    user = request.user
    # 🔹 JWT のトークン無効化（Blacklist に追加）
    try:
        refresh_token = request.data.get("refresh_token")
        if not user.is_2fa_enabled:
            BlacklistedToken.objects.get_or_create(token=token)
        if refresh_token:
            token = RefreshToken(refresh_token)
    except Exception as e:
        return Response({"error": "Invalid refresh token", "detail": str(e)}, status=400)

    return Response({"message": "User logged out and deactivated"}, status=200)
