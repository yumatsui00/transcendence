from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('userinfo/', views.get_user_info, name='get_user_info')
]