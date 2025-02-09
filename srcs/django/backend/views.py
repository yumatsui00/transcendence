from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


# def custom_404_view(request, exception):
#     return render(request, "404.html", status=404)

def landing_page(request):
    return render(request, "index.html") 

def signup_view(request):
	if request.user.is_authenticated:
		return redirect("/home/")  # 🔥 すでにログイン済みなら `/home/` にリダイレクト

	if request.method == "POST": # リクエストがPOSTならいろいろする。GETただの配信
		username = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")
		color = 0
		profile_image = request.FILES.get("profile_image")

		if not username or not email or not password or language is None:
			return error_response("All fields are required")
		#username email の重複チェック
		if CustomUser.objects.filter(username=username).exists():
			return error_response("Username already exists")
		if CustomUser.objects.filter(email=email).exists():
			return error_response("Email already exists")
		# passをハッシュ化して保存
		hashed_password = make_password(password)

		user = CustomUser.objects.create(
			username=username,
			email=email,
			password=password,
			color=0,
			profile_image=profile_image if profile_image else "profile_images/default.png"
		)

		# login(request, user)
		return redirect("/home/")  # 🔥 サインアップ完了後 `/home/` へ

	return render(request, "signup.html")


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


@login_required
def protected_view(request):
    return render(request, "protected.html")