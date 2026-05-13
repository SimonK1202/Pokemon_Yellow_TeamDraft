import pytest
import json
from models import Pokemon


def test_pokemon_initialization():
    # Arrange: Create sample data
    sample_stats = {"hp": 50, "attack": 50, "defense": 50, "special": 50, "speed": 50}

    # Act: Create a Pokemon object
    pika = Pokemon("025", "Pikachu", ["Electric"], sample_stats)

    # Assert: Check if the object is what we expect
    assert pika.name == "Pikachu"
    assert pika.hp == 50
    assert "Electric" in pika.types


def test_library_schema():
    with open("pokemon_library.json", "r") as file:
        data = json.load(file)

    expected_stats = {"hp", "attack", "defense", "special", "speed"}

    for p_id, p_data in data.items():
        # ID-key check
        assert len(p_id) == 3, f"ID {p_id} is not 3 characters long."

        # Name check
        assert "name" in p_data
        assert isinstance(p_data["name"], str)
        assert len(p_data["name"]) > 0, f"Pokemon {p_id} has an empty name."

        # Types check
        assert "types" in p_data
        assert isinstance(p_data["types"], list)
        assert 1 <= len(p_data["types"]) <= 2
        for t in p_data["types"]:
            assert isinstance(t, str) and len(t) > 0

        # Base Stats check
        assert "base_stats" in p_data
        stats = p_data["base_stats"]
        # Verify exactly the 5 expected keys exist
        assert set(stats.keys()) == expected_stats
        for stat_name, value in stats.items():
            assert isinstance(value, int)
            assert value > 0, f"{stat_name} for {p_data['name']} must be positive."