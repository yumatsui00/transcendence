from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=10, unique=True)
	language = models.IntegerField(default=0)
	color = models.IntegerField(default=0)
	profile_image = models.ImageField(upload_to="profile_images/", default="profile_images/default.png")
	# `related_name` を設定して衝突を回避
	groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
	user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True)
	def __str__(self):
		return self.username