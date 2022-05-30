from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

custom_user = get_user_model()

class PokedexPokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PokedexPokemon
        fields = '__all__'

class OwnedPokemonSerializer(serializers.ModelSerializer):

    pokemon = PokedexPokemonSerializer()

    class Meta:
        model = models.OwnedPokemon
        fields = '__all__'

class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = custom_user
        fields = '__all__'

class UnseenPokemonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PokedexPokemon
        fields = ['name']