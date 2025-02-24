"""SSR_DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import landing_page, signup_page, login_page, get_qr_page, home_view


urlpatterns = [
    path('', landing_page, name="landing_page"),
    path('login', login_page, name="login_page"),
    path('signup', signup_page, name="signup_page"),
    path('get_qr/<str:userid>/<str:qr_url>', get_qr_page, name="qr_page"),

    path("home/", home_view, name="home_page"),  # ✅ JWTチェック → `/home/<userid>/` にリダイレクト
#     path("home/<int:userid>/", home_page_with_userid, name="home_page_with_userid"),
]
