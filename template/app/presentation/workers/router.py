from faststream.redis import RedisRouter

from app.presentation.workers.events.sample import router as sample_router

router = RedisRouter()
router.include_router(sample_router)
