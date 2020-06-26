from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class TestingUser(models.Model):
    testid = models.AutoField(primary_key=True)
    name = models.TextField(max_length=20)