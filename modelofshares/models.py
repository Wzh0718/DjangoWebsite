from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# 继承django自带的user，完成后台用户的检验
class UserInfo(AbstractUser):
    account = models.CharField(max_length=128)
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=1024)


class GPData(models.Model):
    managed = True
    id = models.BigIntegerField(primary_key=True)
    date = models.CharField(max_length=128)
    open = models.CharField(max_length=128)
    close = models.CharField(max_length=128)
    lowest = models.CharField(max_length=128)
    highest = models.CharField(max_length=128)


class SessionData(models.Model):
    year = models.CharField(max_length=128)
    y = models.CharField(max_length=128)
    y_pre = models.CharField(max_length=128)
