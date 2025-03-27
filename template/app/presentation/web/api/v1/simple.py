from litestar import get

from app.application.simple.commands import SimpleCommand
from app.application.simple.handlers import SimpleCommandHandler
from app.presentation.web.di import Depends, inject


@get("/simple/")
@inject
async def simple_endpoint(
    interactor: Depends[SimpleCommandHandler],
) -> dict[str, str]:
    result = await interactor(SimpleCommand(number=42))  # noqa: WPS110,WPS432
    return {"message": f"This is a simple endpoint with number: {result}"}
