from litestar import get

from app.application.sample.commands import SampleCommand
from app.application.sample.handlers import SampleCommandHandler
from app.presentation.web.di import Depends, inject


@get("/sample/")
@inject
async def sample_endpoint(
    interactor: Depends[SampleCommandHandler],
) -> dict[str, str]:
    result = await interactor(SampleCommand(number=42))  # noqa: WPS110,WPS432
    return {"message": f"This is a sample endpoint with number: {result}"}
