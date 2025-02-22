from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import requests
import os

def normal_request(url, data):
    try:
        response = requests.post(url, json=data)
        message = response.json().get("message", "Something went wrong")
        return response.status_code, message
    except requests.RequestException as e:
        return None, str(e)



def Register2FAInfo(userid, is_2fa_enabled):
    url = "https://innerproxy/2fa/register-2fa-info/"
    data = {"userid": userid, "is_2fa_enabled": is_2fa_enabled}
    return normal_request(url, data)

