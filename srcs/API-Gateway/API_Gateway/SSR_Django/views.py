from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests
import os


def error_response(message, status=400):
    return JsonResponse({"success": False, "message": message}, status=status)

def error_response_from_other_service(message, ret_status):
    if ret_status is None:
        return error_response(message, status=500)
    return error_response(message, status=400)
    

def success_response(message, data={}):
    return JsonResponse({"success": True, "message": message, **data}, status=200)

# def checkJWT(request):
#     access_token = request.COOKIES.get("access_token")
#     if not access_token:
#         return 403, None

#     headers = {"Authorization": f"Bearer {access_token}"}
#     auth_response = requests.get("https://innerproxy/auth/check-jwt", headers=headers)

#     if auth_response.status == 200:
#         userid = auth_response.json().get("userid")
#         return 200, userid

#     refresh_token = request.COOKIES.get("refresh_token")
#     if refresh_token:
#         refresh_response = request.get("https://innerproxy/auth/refresh", json={"refresh_token": refresh_token})
#         if refresh_response.status_code == 200:
#             new_access_token = refresh_response.json().get("access_token")
#             new_headers = {"Authorization": f"Bearer {new_access_token}"}
#             retry_response = requests.get("https://innerproxy/auth/check-jwt", headers=new_headers)
#             if retry_response.status_code == 200:
#                 userid = retry_response.json().get("userid")
#                 return 200, userid
#     return 403, None


def home_page(request):
    access_token = request.COOKIES.get("access_token")
    
    if not access_token:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    # ✅ API Gateway が `SSR-Django` にリクエストを送る
    headers = {"Authorization": f"Bearer {access_token}"}
    ssr_response = requests.get("https://innerproxy/pages/home/", headers=headers)

    # ✅ `SSR-Django` のレスポンスをそのまま返す
    return HttpResponse(ssr_response.content, status=ssr_response.status_code)