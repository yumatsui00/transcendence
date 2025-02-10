from django.urls import path
from . import views
from .twoFA.views import verify_2fa_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ 追加！

urlpatterns = [
    path('', views.index, name='index'),  # `http://localhost:8000/api/` にアクセスすると `index` が動く
]