import django
import os
import csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poke_project.settings")
django.setup()
from pokemon.models import PokedexPokemon

def populate_pokemon():
    with open('pokemon.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = PokedexPokemon.objects.get_or_create(
                    name=row[0],
                    hp=row[1],
                    attack=row[2],
                    defense=row[3],
                    type=row[4],
                    )

if __name__ == "__main__":
    populate_pokemon()