import logging

# Configure basic logging layout (this usually goes in your entry point, but we'll set it here)
logger = logging.getLogger("TeamDraftLogger")

class PokemonBase:
    """
    Represents a single Pokémon with its base stats from the library.

    Attributes:
        p_id (str): A 3-digit string ID (e.g., "001").
        name (str): The Pokémon's name.
        types (list[str]): 1-2 elemental types.
        hp (int): Base Health Points.
        attack (int): Base Attack Points.
        defense (int): Base Defense Points.
        speed (int): Base Speed Points.
        special_attack (int): Base Special Attack Points.
        special_defense (int): Base Special Defense Points.
    """
    def __init__(self, p_id: str, name: str, types: list[str], base_stats: dict[str, int]):
        self.p_id = p_id
        self.name = name
        self.types = types

        # Stat unpacking with type hints
        self.hp: int = base_stats["hp"]
        self.attack: int = base_stats["attack"]
        self.defense: int = base_stats["defense"]
        self.speed: int = base_stats["speed"]
        self.special_attack: int = base_stats["special_attack"]
        self.special_defense: int = base_stats["special_defense"]

    def __repr__(self) -> str:
        return f"Pokemon({self.p_id}: {self.name})"


class PokemonInstance:
    """A specific Pokémon instance inside a player's team with calculated stats."""

    def __init__(self, base_pokemon: PokemonBase, level: int = 5, current_generation: int = 1):
        self.base = base_pokemon  # Links back to our base blueprint
        self.level = level
        self.moves: list[str] = []  # To hold 1 to 4 move names

        # Calculate stats dynamically on creation
        self.stats = self._calculate_all_stats()

        # Gen 2 Held Item Support with Gen 1 lock
        if current_generation == 1:
            self.item = None
        else:
            self.item = None  # Will default to None, but can be changed later for Gen 2

    def _calculate_all_stats(self) -> dict[str, int]:
        """Calculates all 6 stats based on the base stats and current level."""
        return {
            'hp': int((self.base.hp * 2 * self.level) / 100) + self.level + 10,
            'attack': int((self.base.attack * 2 * self.level) / 100) + 5,
            'defense': int((self.base.defense * 2 * self.level) / 100) + 5,
            'speed': int((self.base.speed * 2 * self.level) / 100) + 5,
            'special_attack': int((self.base.special_attack * 2 * self.level) / 100) + 5,
            'special_defense': int((self.base.special_defense * 2 * self.level) / 100) + 5
        }


class PokemonTeam:
    """A collection of drafted Pokémon organized into 6 fixed positional slots with built-in logging."""

    def __init__(self, name: str):
        self.name: str = name
        self.pokemon_slots: dict[int, PokemonInstance | None] = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None
        }

    def add_pokemon(self, pokemon: PokemonInstance, position: int | None = None) -> None:
        """
        Adds a Pokémon to a slot. If no slot/position is specified, the first free is taken.
        Does not extend the current team size.
        Logs and raises ValueError if the team is full or the slot is unavailable.
        """
        # Case 1: Specific position requested
        if position is not None:
            if position not in self.pokemon_slots:
                msg = f"Team '{self.name}': Invalid position {position}. Slot must be between 1 and 6."
                logger.error(msg)
                raise ValueError(msg)
            if self.pokemon_slots[position] is not None:
                msg = f"Team '{self.name}': Position {position} is already occupied by {self.pokemon_slots[position].base.name}."
                logger.warning(msg)
                raise ValueError(msg)

            self.pokemon_slots[position] = pokemon
            logger.info(f"Team '{self.name}': Successfully added {pokemon.base.name} to position {position}.")
            return

        # Case 2: Default to first open slot
        for slot in range(1, 6):
            if self.pokemon_slots[slot] is None:
                self.pokemon_slots[slot] = pokemon
                logger.info(
                    f"Team '{self.name}': Successfully added {pokemon.base.name} to first open position ({slot}).")
                return

        msg = f"Team '{self.name}': Cannot add {pokemon.base.name}. Team is completely full."
        logger.warning(msg)
        raise ValueError(msg)

    def remove_pokemon(self, position: int) -> None:
        """
        Clears whatever Pokémon is occupying the specified position slot (1-6).
        Logs and raises ValueError if the position is out of bounds or already empty.
        """
        if position not in self.pokemon_slots:
            msg = f"Team '{self.name}': Invalid position {position}. Slot must be between 1 and 6."
            logger.error(msg)
            raise ValueError(msg)
        if self.pokemon_slots[position] is None:
            msg = f"Team '{self.name}': Cannot remove Pokémon. Position {position} is already empty."
            logger.warning(msg)
            raise ValueError(msg)

        removed_poke = self.pokemon_slots[position]
        self.pokemon_slots[position] = None
        logger.info(f"Team '{self.name}': Successfully removed {removed_poke.base.name} from position {position}.")

    def __repr__(self) -> str:
        filled_slots = sum(1 for slot in self.pokemon_slots.values() if slot is not None)
        return f"Team(Name: {self.name}, Filled Slots: {filled_slots}/6)"