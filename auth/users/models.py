from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name= models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.CharField(max_length=200, unique=True)
    password=models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
