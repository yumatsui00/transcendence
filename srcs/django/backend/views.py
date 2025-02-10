from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
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

CustomUser = get_user_model()



# def custom_404_view(request, exception):
#     return render(request, "404.html", status=404)

@api_view(["GET"])
def landing_page(request):
    return render(request, "index.html") 


@api_view(["GET"])
def home_page(request):
    return render(request, "home.html") 

@api_view(["GET"])
def signup_page(request):
    #TODO トークンを持っている→/homeへ
    return render(request, "signup.html")

@api_view(["GET"])
def login_page(request):
    #TODO トークンを持っている→/homeへ
    return render(request, "login.html")

@csrf_exempt
@api_view(["GET"])
def qr_view(request):
	email = request.GET.get("email")
	qr_code_url = request.GET.get("qr_code_url")

	if not email or not qr_code_url:
		return JsonResponse({"error": "Invalid request"}, status=400)

	# ✅ `qr.html` をレンダリング
	return render(request, "qr.html", {"qr_code_url": qr_code_url})


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

	# パスワードのバリデーション（大文字・小文字・数字を含む8文字以上）
	password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
	if not password_regex.match(password):
		return error_response("Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one number.")

	# passをハッシュ化して保存
	hashed_password = make_password(password)

	otp_secret = pyotp.random_base32() if is_2fa_enabled else "" #2FA用のシークレットキーを作成

	user = CustomUser.objects.create(
		username=username,
		email=email,
		password=hashed_password,
		language=language,
		color=0,
		profile_image=profile_image if profile_image else "profile_images/default.png",
		otp_secret=otp_secret,
		is_2fa_enabled=is_2fa_enabled,
	)

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
	return render(request, "otp.html", {"qr_code_url": qr_code_url})



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
        user.last_login = timezone.now()  # ついでに最終ログインも更新
        user.save(update_fields=["is_2fa_verified", "last_login"])  # 最適化

        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):
	try:
		data = json.loads(request.body)
		email = data.get("email")
		password = data.get("password")
		if not email or not password:
			return error_response("Email and Password are required")

		try:
			user = CustomUser.objects.get(email=email)
		except CustomUser.DoesNotExist:
			return error_response("Invalid email or password")

		if not check_password(password, user.password):
			return error_response("Invalid email or password")	

		#ここで2faが行われているか見る
		if user.is_2fa_enabled and not user.is_2fa_verified:
			return success_response("2FA authentication required", {"requires_2fa": True, "email": email, "qr_code_url": user.qr_code_url})

		return success_response("Login Success", {"requires_2fa": False})
	except json.JSONDecodeError:
		return error_response("Invalid JSON")


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def generate_qr(request):
#     user = request.user
    
#     # 2FA シークレットキーがない場合は新規作成
#     if not user.otp_secret:
#         user.otp_secret = pyotp.random_base32()
#         user.save()

#     # Google Authenticator 用の URI を生成
#     totp = pyotp.TOTP(user.otp_secret)
#     otp_uri = totp.provisioning_uri(name=user.email, issuer_name="MyDjangoApp")

#     # QRコードを生成
#     qr = qrcode.make(otp_uri)
#     buf = io.BytesIO()
#     qr.save(buf, format="PNG")
#     buf.seek(0)

#     return HttpResponse(buf.getvalue(), content_type="image/png")





@login_required
def protected_view(request):
    return render(request, "protected.html")