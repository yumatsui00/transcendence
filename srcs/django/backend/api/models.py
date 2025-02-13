from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=10, unique=True)
	language = models.IntegerField(default=0)
	color = models.IntegerField(default=0)
	profile_image = models.ImageField(upload_to="profile_images/", default="profile_images/default.png")

	qr_code_url = models.CharField(max_length=3000, blank=True, null=True)
	otp_secret = models.CharField(max_length=32, blank=True, null=True)  # 2FA シークレットキー
	is_2fa_enabled = models.BooleanField(default=False)  # 2FA が有効かどうか。
	is_2fa_verified = models.BooleanField(default=False)
	temp_login = models.BooleanField(default=False)

	# `related_name` を設定して衝突を回避
	# groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
	# user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)
	def __str__(self):
		return self.username