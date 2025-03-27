from click import Group
from litestar.plugins import CLIPluginProtocol


class ApplicationConfigurator(CLIPluginProtocol):
    """Application configuration plugin."""

    def on_cli_init(self, cli: Group) -> None:
        from app.presentation.cli.shell import shell_cmd

        cli.add_command(shell_cmd)
