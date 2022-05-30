from .serializers import (PokedexPokemonSerializer,
    OwnedPokemonSerializer,
    UnseenPokemonSerializer)
from rest_framework import status
from rest_framework.decorators import (api_view,
    permission_classes,
    authentication_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import OwnedPokemon, PokedexPokemon

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_all_pokemon(request):
    queryset = PokedexPokemon.objects.all()
    serializer = PokedexPokemonSerializer(queryset, many = True)
    return Response(serializer.data, 
                    status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_my_pokemon(request):
    queryset = OwnedPokemon.objects.filter(owner = request.user)
    serializer = OwnedPokemonSerializer(queryset, many = True)
    return Response(serializer.data, 
                    status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def add_pokemon(request):
    pokemon = PokedexPokemon.objects.get(pk=request.data['rand_pokemon'])
    my_pokemon = OwnedPokemon(pokemon = pokemon, owner = request.user)
    my_pokemon.save()
    return Response(data = f"You have a new Pokemon. Your new pokemon is {pokemon.name}", 
                    status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_unowned_pokemon(request):
    seen_pokemon = OwnedPokemon.objects.filter(owner = request.user)
    seen_pokemon_id = seen_pokemon.values_list('pokemon', flat = True)
    queryset = PokedexPokemon.objects.exclude(id__in = list(seen_pokemon_id))
    serializer = UnseenPokemonSerializer(queryset, many = True)
    return Response(serializer.data, 
                    status = status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
def release_pokemon(request):
    try:
        pokemon_ = OwnedPokemon.objects.get(pk=request.data['release_pokemon_id'],
                                            owner=request.user)
    except OwnedPokemon.DoesNotExist:
        return Response("No Pokemon Found", status=status.HTTP_400_BAD_REQUEST)
    
    pokemon_.delete()

    return Response("Your pokemon has been released", status=status.HTTP_204_NO_CONTENT)