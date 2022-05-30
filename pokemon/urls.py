from django.urls import path
from . import views

urlpatterns = [
    path('allpokemon/', views.get_all_pokemon,
         name='get_all_pokemon'), 
    path('unownedpokemon/', views.get_unowned_pokemon,
         name = 'get_unowned_pokemon'), 
    path('addpokemon/', views.add_pokemon, 
         name = 'add_pokemon'), 
    path('mypokemon/', views.get_my_pokemon, 
         name = 'my_pokemon'), 
    path('releasepokemon/', views.release_pokemon,
         name = 'release_pokemon')
]