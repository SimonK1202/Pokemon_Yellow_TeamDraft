import pytest
import json
import logging
from unittest.mock import MagicMock
from models import PokemonBase, PokemonInstance, PokemonTeam


def test_pokemon_initialization():
    # Arrange: Create sample data with split stats
    sample_stats = {
        "hp": 50, "attack": 50, "defense": 50, "speed": 50,
        "special_attack": 50, "special_defense": 50
    }

    # Act: Create a Pokemon object
    pika = PokemonBase("025", "Pikachu", ["Electric"], sample_stats)

    # Assert: Check if the object is what we expect
    assert pika.name == "Pikachu"
    assert pika.hp == 50
    assert pika.special_attack == 50
    assert pika.special_defense == 50
    assert "Electric" in pika.types


@pytest.mark.parametrize("gen_number", [1, 2])
def test_library_schema(gen_number):
    # Dynamically build the file path using the format specifier
    filename = f"pokemon_gen_{gen_number:02d}.json"

    with open(filename, "r") as file:
        data = json.load(file)

    # Metadata check - ensures the internal metadata matches the filename
    assert "metadata" in data
    assert data["metadata"]["generation"] == gen_number

    # Expected stat keys for modern split architecture
    expected_stats = {"hp", "attack", "defense", "speed", "special_attack", "special_defense"}

    # Loop through the nested "pokemon" list
    assert "pokemon" in data
    for p_data in data["pokemon"]:
        p_id = p_data["id"]

        # ID-key check
        assert len(p_id) == 3, f"ID {p_id} in {filename} is not 3 characters long."

        # Name check
        assert "name" in p_data
        assert isinstance(p_data["name"], str)
        assert len(p_data["name"]) > 0, f"Pokemon {p_id} in {filename} has an empty name."

        # Types check
        assert "types" in p_data
        assert isinstance(p_data["types"], list)
        assert 1 <= len(p_data["types"]) <= 2
        for t in p_data["types"]:
            assert isinstance(t, str) and len(t) > 0

        # Base Stats check
        assert "base_stats" in p_data
        stats = p_data["base_stats"]

        # Verify exactly the 6 expected keys exist
        assert set(stats.keys()) == expected_stats
        for stat_name, value in stats.items():
            assert isinstance(value, int)
            assert value > 0, f"{stat_name} for {p_data['name']} in {filename} must be positive."


def test_pokemon_instance_stat_calculation():
    # 1. Create a dummy base (using Pikachu's actual Gen 1 split stats)
    pikachu_base = PokemonBase(
        p_id="025",
        name="Pikachu",
        types=["Electric"],
        base_stats={
            "hp": 35, "attack": 55, "defense": 30, "speed": 90,
            "special_attack": 50, "special_defense": 50
        }
    )

    # 2. Instantiate a Level 50 Pikachu (Defaults to generation 1)
    pika_lv50 = PokemonInstance(base_pokemon=pikachu_base, level=50, current_generation=1)

    # 3. Assert the math matches Gen 1 expectations
    # HP calculation check via the stats dictionary directly
    # HP: int((35 * 2 * 50) / 100) + 50 + 10 = 35 + 50 + 10 = 95
    assert pika_lv50.stats["hp"] == 95

    # Attack & Speed checks
    assert pika_lv50.stats["attack"] == 60
    assert pika_lv50.stats["speed"] == 95

    # Split stat checks
    assert pika_lv50.stats["special_attack"] == 55
    assert pika_lv50.stats["special_defense"] == 55

    # 4. Assert Gen 1 held item constraint is enforced
    assert pika_lv50.item is None


@pytest.fixture
def mock_pokemon():
    """Provides a dummy PokemonInstance mock to avoid loading JSONs for team tests."""
    mock_poke = MagicMock()
    mock_poke.base.name = "Pikachu"
    return mock_poke


@pytest.fixture
def empty_team():
    """Provides a fresh, empty PokemonTeam for every test execution."""
    return PokemonTeam(name="Pallet Town Challengers")


### 1. Test Add Functionality
def test_add_pokemon_first_available_slot(empty_team, mock_pokemon):
    """Verifies that adding a Pokémon defaults to filling the first open numerical slot."""
    empty_team.add_pokemon(mock_pokemon)
    assert empty_team.pokemon_slots[1] is mock_pokemon
    assert empty_team.pokemon_slots[2] is None


def test_add_pokemon_specific_slot(empty_team, mock_pokemon):
    """Verifies that passing an explicit position argument locks the Pokémon to that spot."""
    empty_team.add_pokemon(mock_pokemon, position=4)
    assert empty_team.pokemon_slots[4] is mock_pokemon
    assert empty_team.pokemon_slots[1] is None


### 2. Test Roster Size Guardrails (Strictly at most 6)
def test_add_pokemon_to_completely_full_team(empty_team, mock_pokemon):
    """Verifies that a team caps out at 6 and throws a ValueError on the 7th attempt."""
    # Fill up all 6 positions
    for _ in range(6):
        empty_team.add_pokemon(mock_pokemon)

    # Verify the 7th add raises a ValueError
    with pytest.raises(ValueError) as exc_info:
        empty_team.add_pokemon(mock_pokemon)

    # FORCE the exception value to a pure string before running assertions
    error_message = str(exc_info.value)

    assert "Team is completely full" in error_message


def test_add_pokemon_invalid_out_of_bounds_slot(empty_team, mock_pokemon):
    """Verifies that passing a slot number outside of 1-6 raises an explicit ValueError."""
    with pytest.raises(ValueError) as exc_info:
        empty_team.add_pokemon(mock_pokemon, position=7)

    assert "Slot must be between 1 and 6" in str(exc_info.value)


def test_add_pokemon_slot_already_occupied(empty_team, mock_pokemon):
    """Verifies that attempting to overwrite an occupied slot raises an error."""
    empty_team.add_pokemon(mock_pokemon, position=3)

    with pytest.raises(ValueError) as exc_info:
        empty_team.add_pokemon(mock_pokemon, position=3)

    assert "already occupied" in str(exc_info.value)


### 3. Test Remove Functionality
def test_remove_pokemon_successfully(empty_team, mock_pokemon):
    """Verifies that removing an item clears the specific numerical position."""
    empty_team.add_pokemon(mock_pokemon, position=2)
    assert empty_team.pokemon_slots[2] is mock_pokemon

    empty_team.remove_pokemon(position=2)
    assert empty_team.pokemon_slots[2] is None


def test_remove_pokemon_from_already_empty_slot(empty_team):
    """Verifies that attempting to clear an already vacant slot triggers an error gracefully."""
    with pytest.raises(ValueError) as exc_info:
        empty_team.remove_pokemon(position=5)

    assert "already empty" in str(exc_info.value)