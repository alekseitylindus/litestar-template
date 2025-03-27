from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app.__about__ import __version__ as current_version
from app.config.base import Settings


def get_openapi_config(settings: Settings) -> OpenAPIConfig:
    """OpenAPI config for app.  See OpenAPISettings for configuration."""
    return OpenAPIConfig(
        title=settings.app.name,
        version=current_version,
        use_handler_docstrings=True,
        render_plugins=[ScalarRenderPlugin()],
    )
