from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=10, unique=True)
	language = models.IntegerField(default=0)
	color = models.IntegerField(default=0)
	profile_image = models.ImageField(upload_to="profile_images/", default="profile_images/default.png")

	qr_code_url = models.CharField(max_length=3000, blank=True, null=True)
	otp_secret = models.CharField(max_length=32, blank=True, null=True)  # 2FA シークレットキー
	is_2fa_enabled = models.BooleanField(default=False)  # 2FA が有効かどうか。
	is_registered_once = models.BooleanField(default=False)

	# `related_name` を設定して衝突を回避
	# groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
	# user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)
	def __str__(self):
		return self.username

def get_default_expiration():
    return timezone.now() + timedelta(days=7)

# refreshtokenの保存をユーザ内で行うと、ユーザに対し一つのトークンしか保存できず、別デバイスからのログインが面倒
class RefreshTokenStore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_expiration)
    ip_address = models.GenericIPAddressField()  # 追加: IPアドレス
    device_name = models.CharField(max_length=255)  # 追加: デバイス名

    def is_valid(self):
        """ トークンの有効期限チェック """
        return self.expires_at > timezone.now()