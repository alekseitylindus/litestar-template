import logging
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from math import ceil
from typing import Any

from litestar import Request
from litestar.exceptions import TooManyRequestsException
from redis.asyncio import Redis

UserIdentifier = Callable[[Request[Any, Any, Any]], Coroutine[Any, Any, str]]  # noqa: WPS221
HttpCallback = Callable[
    [Request[Any, Any, Any], int],
    Coroutine[Any, Any, None],
]

logger = logging.getLogger(__name__)


async def default_identifier(request: Request[Any, Any, Any]) -> str:
    """
    Generates a unique identifier for a request based on the client's IP address and the request path.

    The function first checks for the "X-Forwarded-For" header to get the client's IP address. If this header is not present,
    it falls back to the IP address from the request's client information. The IP address is then concatenated with the request path.

    Args:
        request (Request[Any, Any, Any]): The incoming request object.

    Returns:
        str: A string that combines the client's IP address and the request path.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    ip = (
        forwarded.split(",")[0]
        if forwarded
        else (request.client and request.client.host) or ""
    )
    identifier = f"{ip}:{request.scope['path']}"
    logger.info("Rate limit identifier: %s", identifier)
    return identifier


async def default_callback(request: Request[Any, Any, Any], pexpire: int) -> None:  # noqa: ARG001
    """
    Handles the default HTTP callback for rate limiting.

    This function is called when a rate limit is exceeded. It raises a
    TooManyRequestsException with a message indicating that the rate limit
    has been exceeded and includes a 'Retry-After' header specifying the
    time (in seconds) after which the client can retry the request.

    Args:
        request (Request[Any, Any, Any]): The incoming HTTP request.
        pexpire (int): The time in milliseconds after which the rate limit
                       will expire.

    Raises:
        TooManyRequestsException: Indicates that the rate limit has been
                                  exceeded.
    """
    expire = ceil(pexpire / 1000)
    raise TooManyRequestsException(
        detail="Rate limit exceeded.",
        headers={"Retry-After": str(expire)},
    )


class RateLimiter:
    lua_script = """local key = KEYS[1]
local limit = tonumber(ARGV[1])
local expire_time = ARGV[2]

local current = tonumber(redis.call('get', key) or "0")
if current > 0 then
 if current + 1 > limit then
 return redis.call("PTTL",key)
 else
        redis.call("INCR", key)
 return 0
 end
else
    redis.call("SET", key, 1,"px",expire_time)
 return 0
end"""

    def __init__(
        self,
        redis: Redis,
        prefix: str,
        lua_sha: str,
        identifier: UserIdentifier,
        callback: HttpCallback,
    ) -> None:
        self.redis = redis
        self.prefix = prefix
        self.lua_sha = lua_sha
        self.identifier = identifier
        self.callback = callback

    async def __call__(  # noqa: WPS210 Ok here
        self,
        request: Request[Any, Any, Any],
        times: int,
        milliseconds: int,
        identifier: UserIdentifier | None = None,
        callback: HttpCallback | None = None,
    ) -> None:
        identifier = identifier or self.identifier
        callback = callback or self.callback
        rate_key = await identifier(request)
        view_id = request.route_handler.handler_id
        key = f"{self.prefix}:{rate_key}:{view_id}"
        pexpire = await self._check(key, times, milliseconds)
        if pexpire != 0:
            await callback(request, pexpire)

    @classmethod
    async def setup(
        cls,
        redis: Redis,
        prefix: str,
        identifier: UserIdentifier | None = None,
        callback: HttpCallback | None = None,
    ) -> "RateLimiter":
        lua_sha = await redis.script_load(cls.lua_script)
        return cls(
            redis,
            prefix,
            lua_sha,
            identifier or default_identifier,
            callback or default_callback,
        )

    async def _check(self, key: str, times: int, millisecods: int) -> int:
        pexpire = await self.redis.evalsha(
            self.lua_sha,
            1,
            key,
            str(times),
            str(millisecods),
        )  # type: ignore  # noqa: PGH003
        return int(pexpire)


@dataclass
class RateLimit:
    times: int = 1
    milliseconds: int = 0
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    identifier: UserIdentifier | None = None
    callback: HttpCallback | None = None

    @property
    def total_ms(self) -> int:
        return (
            self.milliseconds
            + 1000 * self.seconds
            + 60000 * self.minutes  # noqa: WPS432
            + 3600000 * self.hours  # noqa: WPS432
        )
