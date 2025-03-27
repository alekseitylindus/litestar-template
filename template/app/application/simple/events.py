from dataclasses import dataclass

from app.application.common.event import Event


@dataclass(frozen=True, kw_only=True)
class SimpleNumberRequestedEvent(Event):
    input_number: int
    result: int  # noqa: WPS110
