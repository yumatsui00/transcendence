from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AuthUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import re
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

def error_response(message, status=400):
    return JsonResponse({"success": False, "message": message}, status=status)

def success_response(message, data={}):
    return JsonResponse({"success": True, "message": message, **data}, status=200)

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,200}$"

def validate_password(password):
    print("checking password...")
    return bool(re.match(PASSWORD_REGEX, password))

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def password_check(request):
    password = request.data.get("password")
    if not password or not validate_password(password):
        return error_response("Invalid Password")
    return success_response("Valid Password")


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    try:
        data = json.loads(request.body)
        userid = data.get("userid")
        password = data.get("password")

        if not password or not validate_password(password):
            return error_response("Invalid password")
        if not userid:
            return error_response("Couldn't assign user id for some reasons")

        auth_user = AuthUser(userid=userid)
        auth_user.set_password(password)
        auth_user.save()

        print(f"Debug: User registered successfully with userid={userid}")  # ✅ ログ追加

        return success_response("User Registered successfully")

    except json.JSONDecodeError:
        return error_response("Invalid JSON format")
    except Exception as e:
        print(f"Error in register: {e}")  # ✅ 例外ログ
        return error_response(str(e))



@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def AuthPassword(request):
    try:
        data = json.loads(request.body)
        userid = data.get("userid")
        password = data.get("password")

        if not userid or not password:
            return error_response("userid and password are required")

        # ✅ `userid` に該当するユーザーを取得
        auth_user = AuthUser.objects.filter(userid=userid).first()
        
        if not auth_user:
            return error_response("User not found")

        # ✅ パスワードチェック
        if not auth_user.check_password(password):
            return error_response("Invalid password")

        print(f"Debug: Authentication successful for userid={userid}")  # ✅ デバッグログ

        return success_response("Authentication successful")

    except json.JSONDecodeError:
        return error_response("Invalid JSON format")
    except Exception as e:
        print(f"Error: {e}")  # ✅ エラーログを追加
        return error_response(str(e))


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def GetToken(request):
    try:
        data = request.data
        userid = data.get("userid")
        if not userid:
            return error_response("Userid Missing")
        user = AuthUser.objects.get(userid=userid)  # `AuthUser` から `userid` に一致するユーザーを取得
        if not user:
            return error_response("User is Missing")

        refresh = RefreshToken.for_user(user)   # `user` を渡す
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return success_response("Token created successfully", data={"access_token": access_token, "refresh_token": refresh_token})
    except Exception as e:
        return error_response(str(e))


@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def CheckJWT(request):
    user = request.user
    return success_response("this user is authenticated", data={"userid": user.userid })


