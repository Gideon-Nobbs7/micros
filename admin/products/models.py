from django.db import models


# Create your models here.
class Fare(models.Model):
    location = models.CharField(max_length=200)
    price = models.IntegerField()
    difficulty = models.CharField(max_length=200)


class User(models.Model):
    pass
