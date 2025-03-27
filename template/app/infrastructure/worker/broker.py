from faststream.redis import RedisBroker


def get_broker(url: str, db: int = 1) -> RedisBroker:
    return RedisBroker(url, db=db)
