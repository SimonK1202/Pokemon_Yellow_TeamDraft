import pytest
# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()
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