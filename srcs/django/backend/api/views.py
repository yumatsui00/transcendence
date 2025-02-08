from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .utils import error_response, success_response
import json


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
			#migrateをしていたら、createだけでpostgresにユーザを登録可能
			return success_response("User created successfully")

		except Exception as e:
			return error_response(str(e), status=500)

	return error_response("Invalid request method", status=405)