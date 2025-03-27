from dataclasses import dataclass

from app.application.common.command import Command


@dataclass(frozen=True)
class SimpleCommand(Command):
    number: int
