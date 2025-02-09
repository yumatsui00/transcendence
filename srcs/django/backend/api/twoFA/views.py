from django_otp.oath import totp
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def verify_2fa_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            otp_code = data.get("otp")

            user = User.objects.get(username=username)
            device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

            if not device:
                return error_response("2FA is not set up for this user")

            # 現在の OTP コードを取得
            valid_otp = totp(device.bin_key, step=device.step, digits=device.digits)

            if otp_code == str(valid_otp):
                return success_response("2FA verification successful")
            else:
                return error_response("Invalid OTP code")

        except Exception as e:
            return error_response(str(e), status=500)

    return error_response("Invalid request method", status=405)