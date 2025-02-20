from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class AuthUser(models.Model):
    userid = models.IntegerField(unique=True)
    password_hash = models.CharField(max_length=255)

    def set_password(self, password):
        """passwordをハッシュ化して保存"""
        self.password_hash = make_password(password)

    def check_password(self, password):
        """passwordをcheck"""
        return check_password(password, self.password_hash)

    def __str__(self):
        return f"AuthUser {self.userid}"

