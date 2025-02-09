from django.http import JsonResponse

def error_response(message, status=400):
    """JSON形式のエラーレスポンスを簡単に作成"""
    return JsonResponse({"success": False, "message": message}, status=status)

def success_response(message, data={}):
    return JsonResponse({"success": True, "message": message, **data}, status=200)
