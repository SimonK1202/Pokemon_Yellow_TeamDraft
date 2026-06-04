import json
from models import PokemonBase


def load_pokemon_library(generation: int) -> list[PokemonBase]:
    # Dynamically build the filename using 2-digit integer padding (:02d)
    filename = f"pokemon_gen_{generation:02d}.json"

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            pokemon_list = data["pokemon"]

            return [
                PokemonBase(
                    p_id=poke_data["id"],
                    name=poke_data["name"],
                    types=poke_data["types"],
                    base_stats=poke_data["base_stats"]
                )
                for poke_data in pokemon_list
            ]
    except FileNotFoundError:
        print(f"Data file '{filename}' not found for Generation {generation}.")
        return []


if __name__ == "__main__":
    # The generation setter lives here in the main block now!
    CURRENT_GENERATION = 1

    pokemon_library_list = load_pokemon_library(generation=CURRENT_GENERATION)
    print(f"--- Loaded Generation {CURRENT_GENERATION} Library ---")
    for poke in pokemon_library_list:
        print(poke)