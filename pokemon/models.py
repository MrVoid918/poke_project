from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, 
    PermissionsMixin,
    BaseUserManager)
from random import randint

def generate_level():
    return randint(1, 100)

# Create your models here.
class PokedexPokemon(models.Model):
    name = models.CharField(max_length=255)
    hp = models.PositiveIntegerField()
    attack = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OwnedPokemon(models.Model):
    pokemon = models.ForeignKey(PokedexPokemon, models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    #level = models.PositiveIntegerField(default = generate_level)

class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password = None):

        if not email or not username:
            raise ValueError("User must have email address and username")

        email = self.normalize_email(email)
        user = self.model(username = username, email = email)

        user.set_password(password)
        user.save()

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique = True)
    email = models.EmailField(max_length=255, unique = True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'password']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username