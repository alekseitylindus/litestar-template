from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
"""Base directory of the project."""
APP_DIR = BASE_DIR / "app"
"""App directory."""
STATIC_DIR = BASE_DIR / "public"
"""Static directory."""
TEMPLATES_DIR = APP_DIR / "presentation" / "web" / "templates"
"""Templates directory."""
