"""backend URL Configuration

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
from django.urls import path, include
from .views import signup_view, verify_otp, qr_view, otp_view, login_view, check_auth, logout_view
from rest_framework_simplejwt.views import TokenRefreshView
from .render import landing_page, signup_page, login_page, home_page, setting_page, matchmaking_page, matchgame_page
urlpatterns = [
    path("", landing_page, name="landing_page"),
    path('admin/', admin.site.urls),
    path('signup/', signup_page, name='signup_page'),
    path('login/', login_page, name='login_page'),
    path('home/', home_page, name='home_page'),
    path('home/setting/', setting_page, name='setting_page'),
    path('matchmaking/', matchmaking_page, name='matchmaking_page'),
    path('match-game/<str:room_name>/', matchgame_page, name='matchgame_page'),
    path('authenticator/signup/', signup_view, name='signup'),
    path('authenticator/verify_otp/', verify_otp, name='verify_otp'),
    path('authenticator/qr/', qr_view, name='qr_view'),
    path('authenticator/otp/', otp_view, name='verify_otp'),
    path('authenticator/login/', login_view, name='login_view'),
    path("authenticator/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('authenticator/check_auth/', check_auth, name="check_auth"),
    path('authenticator/logout/', logout_view, name="logout_view"),

    # path('protected/', protected_view, name='protected'),
    # path('generate_qr/', generate_qr, name='generate_qr'),
    # path('verify_otp/', verify_otp, name='verify_otp'),
    path('api/', include('backend.api.urls')),  # 👈 `/api/` のリクエストを `api.urls.py` に転送
]

# handler404 = "backend.views.custom_404_view"