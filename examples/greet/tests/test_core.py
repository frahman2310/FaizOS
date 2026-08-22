"""Note the import: `from greet import greet`, never `from src.greet import greet`."""

from greet import greet


def test_plain_greeting():
    assert greet("Faiz") == "Hello, Faiz."


def test_excited_greeting():
    assert greet("Faiz", excited=True) == "Hello, Faiz!"
