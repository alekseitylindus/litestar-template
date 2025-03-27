from collections.abc import Mapping
from functools import partial
from typing import Any, cast

from litestar.connection import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template import TemplateConfig
from litestar.template.base import csrf_token, url_for

from app.config.base import Settings
from app.config.constants import TEMPLATES_DIR


def register_template_callables(
    settings: Settings,  # noqa: ARG001
    engine: JinjaTemplateEngine,
) -> None:
    # unregister predefined template callables
    engine.engine.globals.pop("url_for_static_asset", None)
    engine.engine.globals.pop("url_for", None)

    engine.register_template_callable(
        key="static",
        template_callable=_static,
    )
    engine.register_template_callable(key="csrf_token", template_callable=csrf_token)
    engine.register_template_callable(key="url", template_callable=url_for)


def get_template_config(settings: Settings) -> TemplateConfig[JinjaTemplateEngine]:
    template_config = TemplateConfig(
        directory=TEMPLATES_DIR,
        engine=JinjaTemplateEngine,
        engine_callback=partial(register_template_callables, settings),
    )
    return template_config


def _static(context: Mapping[str, Any], /, file_path: str) -> str:
    """Wrap default"""
    request = cast(Request[Any, Any, Any], context["request"])
    return request.app.route_reverse(name="static", file_path=file_path)
