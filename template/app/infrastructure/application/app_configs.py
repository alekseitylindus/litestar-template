from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig

from app.config.base import Settings


def get_compression_config(settings: Settings) -> CompressionConfig:  # noqa: ARG001
    return CompressionConfig(backend="gzip")


def get_csrf_config(settings: Settings) -> CSRFConfig:
    return CSRFConfig(
        secret=settings.app.secret_key,
        cookie_secure=settings.app.csrf_cookie_secure,
        cookie_name=settings.app.csrf_cookie_name,
        header_name=settings.app.csrf_header_name,
    )


def get_cors_config(settings: Settings) -> CORSConfig:
    return CORSConfig(allow_origin_regex=settings.app.allow_origin_regex)
