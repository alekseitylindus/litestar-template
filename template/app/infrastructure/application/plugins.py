from litestar.plugins import PluginProtocol
from litestar_vite import ViteConfig, VitePlugin

from app.config.base import Settings
from app.config.constants import BASE_DIR
from app.infrastructure.application.configurator import ApplicationConfigurator


def get_plugins(settings: Settings) -> list[PluginProtocol]:
    plugins: list[PluginProtocol] = [
        ApplicationConfigurator(),
        VitePlugin(
            config=ViteConfig(
                bundle_dir=BASE_DIR / "public",
                resource_dir=BASE_DIR / "resources",
                public_dir=BASE_DIR / "public",
                is_react=True,
                hot_reload=settings.app.debug,
                dev_mode=settings.app.debug,
            ),
        ),
    ]
    return plugins
