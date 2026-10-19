"""Tiny helper for reading API keys from the environment."""

import os


def require_env(name: str) -> str:
    """Return the value of environment variable ``name`` or fail with a clear message."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"{name} is not set. Copy .env.example to .env and fill it in, "
            "or export the variable in your shell."
        )
    return value
