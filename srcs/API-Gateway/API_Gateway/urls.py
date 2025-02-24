"""API_Gateway URL Configuration

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
from django.urls import path
from .views import signup_view, login_view, logout_view
from .SSR_Django.views import landing_page_view, signup_page_view, login_page_view, home_page, setting_page
# from .twoFAService.views import generate_qr_view

urlpatterns = [
    path('api/signup/', signup_view, name="signup_view"),
    path('api/login/', login_view, name="login_view"),
    path('api/logout/', logout_view, name="logout_view"),

    # SSR-Django用。COOKIE保存のため認証ページはapigateway経由
    path('', landing_page_view, name="landing_page"),
    path('signup/', signup_page_view, name="signup_page"),
    path('login/', login_page_view, name="login_page"),
    path('pages/home/', home_page, name="home_page"),
    path('pages/setting/', setting_page, name="setting_page"),
]
