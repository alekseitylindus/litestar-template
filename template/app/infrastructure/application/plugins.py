from litestar.plugins import PluginProtocol

from app.config.base import Settings
from app.infrastructure.application.configurator import ApplicationConfigurator


def get_plugins(settings: Settings) -> list[PluginProtocol]:
    plugins: list[PluginProtocol] = [
        ApplicationConfigurator(),
    ]
    return plugins
