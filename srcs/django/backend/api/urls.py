from django.urls import path
from . import views
from .twoFA.views import verify_2fa_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ 追加！

urlpatterns = [
    path('', views.index, name='index'),  # `http://localhost:8000/api/` にアクセスすると `index` が動く
    path('signup/', views.signup_view, name='signup'),

    path('jwt/', TokenObtainPairView.as_view(), name='jwt'),  # JWTのログイン
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWTリフレッシュ
    path('2FA/verify', verify_2fa_view, name='2fa'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),  # 認証ユーザー限定ページ
]