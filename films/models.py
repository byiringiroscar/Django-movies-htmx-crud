from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Film(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='films') # this related will help us to get all films of a user like user.films.all()

    def __str__(self):
        return self.name