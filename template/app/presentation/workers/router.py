from faststream.redis import RedisRouter

from app.presentation.workers.events.simple import router as simple_router

router = RedisRouter()
router.include_router(simple_router)
