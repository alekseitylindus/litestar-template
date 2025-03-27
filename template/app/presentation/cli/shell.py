from __future__ import annotations

import click
import IPython
from traitlets.config import Config

config = Config()

config.InteractiveShellApp.exec_lines = [
    "from dishka import make_async_container",
    "from app.config.base import Settings, get_settings",
    "from app.config.constants import *",
    "from app.infrastructure.di.registry import get_providers",
    "settings = get_settings()",
    "container = make_async_container(*get_providers(), context={Settings: settings})",
]
config.InteractiveShell.confirm_exit = True
config.TerminalIPythonApp.display_banner = False


@click.command(
    name="shell",
    help="Run application shell.",
)
@click.pass_context
def shell_cmd(_: click.Context) -> None:
    """Run application shell."""
    IPython.start_ipython(config=config, argv=[])  # type: ignore[no-untyped-call]
