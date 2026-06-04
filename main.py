import json
from models import Pokemon

def load_pokemon_library():
    try:
        with open("pokemon_gen_01.json", "r") as file:
            data = json.load(file)
            # Convert dictionary items into a list of Pokemon Objects
            return [Pokemon(k, v["name"], v["types"], v["base_stats"]) for k, v in data.items()]
    except FileNotFoundError:
        print("Data file not found.")
        return []

if __name__ == "__main__":
    pokemon_library_list = load_pokemon_library()
    for poke in pokemon_library_list:
        print(poke)

