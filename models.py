class PokemonBase:
    """
    Represents a single Pokemon with its base stats from the library.

    Attributes:
        p_id (str): A 3-digit string ID (e.g., "001").
        name (str): The Pokemon's name.
        types (list[str]): 1-2 elemental types.
        hp (int): Base Health Points.
        attack (int): Base Attack Points.
        defense (int): Base Defense Points.
        special (int): Base Special Points.
        speed (int): Base Speed Points.
        ...
    """
    def __init__(self, p_id: str, name: str, types: list[str], base_stats: dict[str, int]):
        self.p_id = p_id
        self.name = name
        self.types = types

        # Stat unpacking with type hints
        self.hp: int = base_stats["hp"]
        self.attack: int = base_stats["attack"]
        self.defense: int = base_stats["defense"]
        self.special: int = base_stats["special"]
        self.speed: int = base_stats["speed"]

    def __repr__(self) -> str:
        return f"Pokemon({self.p_id}: {self.name})"


class PokemonInstance:
    """A specific Pokémon instance inside a player's team with calculated stats."""

    def __init__(self, base_pokemon: PokemonBase, level: int = 5):
        self.base = base_pokemon  # Links back to our base blueprint
        self.level = level
        self.moves: list[str] = []  # To hold 1 to 4 move names

        # Calculate stats dynamically on creation
        self.stats = self._calculate_all_stats()
        self.max_hp = self.stats["hp"]

    def _calculate_all_stats(self) -> dict[str, int]:
        """Calculates all 5 stats based on the base stats and current level."""
        calculated = {
            'hp':       int((self.base.hp * 2 * self.level) / 100) + self.level + 10,
            'attack':   int((self.base.attack * 2 * self.level) / 100) + 5,
            'defense':  int((self.base.defense * 2 * self.level) / 100) + 5,
            'special':  int((self.base.special * 2 * self.level) / 100) + 5,
            'speed':    int((self.base.speed * 2 * self.level) / 100) + 5}

        return calculated