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
		otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=email, issuer_name="MyApp")
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





def login_view(request):
    if request.user.is_authenticated:
        return redirect("/home/")  # 🔥 すでにログイン済みなら `/home/` にリダイレクト

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home/")  # 🔥 ログイン成功なら `/home/` へ

    return render(request, "login.html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_qr(request):
    user = request.user
    
    # 2FA シークレットキーがない場合は新規作成
    if not user.otp_secret:
        user.otp_secret = pyotp.random_base32()
        user.save()

    # Google Authenticator 用の URI を生成
    totp = pyotp.TOTP(user.otp_secret)
    otp_uri = totp.provisioning_uri(name=user.email, issuer_name="MyDjangoApp")

    # QRコードを生成
    qr = qrcode.make(otp_uri)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return HttpResponse(buf.getvalue(), content_type="image/png")


@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp_input = request.data.get("otp")

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=400)

    # OTP を検証
    totp = pyotp.TOTP(user.otp_secret)
    if not totp.verify(otp_input):
        return JsonResponse({"error": "Invalid OTP"}, status=400)

    # 認証成功 → 2FA 有効化
    user.is_2fa_enabled = True
    user.save()

    # JWT トークンを発行
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        "message": "2FA verification successful",
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh)
    }, status=200)

@login_required
def protected_view(request):
    return render(request, "protected.html")