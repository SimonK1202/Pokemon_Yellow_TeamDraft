class Pokemon:
    """
    Represents a single Pokemon with its base stats from the library.

    Attributes:
        id (str): A 3-digit string ID (e.g., "001").
        name (str): The Pokemon's name.
        types (list[str]): 1-2 elemental types.
        hp (int): Base Health Points.
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