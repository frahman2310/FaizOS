"""The actual work. One function, typed, with a docstring that says what it returns."""


def greet(name: str, excited: bool = False) -> str:
    """Return a greeting for `name`. Adds an exclamation mark when `excited`."""
    ending = "!" if excited else "."
    return f"Hello, {name}{ending}"
