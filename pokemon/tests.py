import json
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from .models import PokedexPokemon, CustomUser, OwnedPokemon
from .serializers import PokedexPokemonSerializer, OwnedPokemonSerializer
from rest_framework import status
from .populate_pokemon import populate_pokemon
# Create your tests here.

client = APIClient()

class GetAllPokemonTest(TestCase):

    def setUp(self) -> None:
        populate_pokemon()
        CustomUser.objects.create_user("myusername", "testingmail@mail.com", "qwertykeyboard")

    def test_get_all_pokemon_w_o_auth(self):
        response = client.get(reverse('get_all_pokemon'))
        pokedexpokemon = PokedexPokemon.objects.all()
        serializer = PokedexPokemonSerializer(pokedexpokemon, many = True)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_pokemon_w_auth(self):
        user = CustomUser.objects.get(username="myusername")
        client.force_authenticate(user = user)
        response = client.get(reverse('get_all_pokemon'))
        pokedexpokemon = PokedexPokemon.objects.all()
        serializer = PokedexPokemonSerializer(pokedexpokemon, many = True)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data and serializer.data)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.force_authenticate(user=None)

class CreatePokemonTest(TestCase):

    def setUp(self) -> None:
        populate_pokemon()
        CustomUser.objects.create_user("myusername", "testingmail@mail.com", "qwertykeyboard")

    def test_create_pokemon_w_o_auth(self):
        response = client.post(reverse('add_pokemon'), {'rand_pokemon': 1}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pokemon_w_auth(self):
        user = CustomUser.objects.get(username="myusername")
        client.force_authenticate(user = user)
        response = client.post(reverse('add_pokemon'), {'rand_pokemon': 1}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(OwnedPokemon.objects.filter(id = 1).exists())
        self.assertTrue(OwnedPokemon.objects.get(id = 1).owner == user)
        client.force_authenticate(user=None)

class GetMyPokemonTest(TestCase):

    def setUp(self) -> None:
        populate_pokemon()
        CustomUser.objects.create_user("myusername1", "testingmail1@mail.com", "qwertykeyboard")
        CustomUser.objects.create_user("myusername2", "testingmail2@mail.com", "qwertykeyboard")
        self.user1 = CustomUser.objects.get(username="myusername1")
        self.user2 = CustomUser.objects.get(username="myusername2")
        pokemon_1 = PokedexPokemon.objects.get(id=1)
        pokemon_2 = PokedexPokemon.objects.get(id=2)
        self.owned_pokemon_1 = OwnedPokemon.objects.create(pokemon = pokemon_1,
                                                           owner = self.user1)
        self.owned_pokemon_2 = OwnedPokemon.objects.create(pokemon = pokemon_2,
                                                           owner = self.user2)

    def test_get_pokemon_w_o_auth(self):
        client.force_authenticate(user=None)
        response = client.get(reverse('my_pokemon'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_pokemon_w_auth(self):
        client.force_authenticate(user = self.user1)
        response = client.get(reverse('my_pokemon'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = OwnedPokemonSerializer(self.owned_pokemon_1)
        
        self.assertEqual(response.data[0], serializer.data)
        
class ReleasePokemonTest(TestCase):

    def setUp(self) -> None:
        populate_pokemon()
        CustomUser.objects.create_user("myusername1", "testingmail1@mail.com", "qwertykeyboard")
        CustomUser.objects.create_user("myusername2", "testingmail2@mail.com", "qwertykeyboard")
        self.user1 = CustomUser.objects.get(username="myusername1")
        self.user2 = CustomUser.objects.get(username="myusername2")
        pokemon_1 = PokedexPokemon.objects.get(id=1)
        pokemon_2 = PokedexPokemon.objects.get(id=2)
        self.owned_pokemon_1 = OwnedPokemon.objects.create(pokemon = pokemon_1, owner = self.user1)
        self.owned_pokemon_2 = OwnedPokemon.objects.create(pokemon = pokemon_2, owner = self.user2)

    def test_delete_w_o_auth(self):
        client.force_authenticate(None)
        response = client.delete(reverse('release_pokemon'), {'release_pokemon_id': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_w_diff_auth_pokemon(self):
        client.force_authenticate(user = self.user1)
        response = client.delete(reverse('release_pokemon'), {'release_pokemon_id': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_w_auth(self):
        client.force_authenticate(user = self.user2)
        response = client.delete(reverse('release_pokemon'), {'release_pokemon_id': 2}, format='json')
        self.assertEqual("Your pokemon has been released", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)