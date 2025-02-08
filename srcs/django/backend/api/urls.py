from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # `http://localhost:8000/api/` にアクセスすると `index` が動く
]