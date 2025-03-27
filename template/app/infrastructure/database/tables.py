import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    mapped_column,
    registry,
)

mapper_registry = registry(
    type_annotation_map={
        uuid.UUID: sa.UUID(as_uuid=True),
        datetime: sa.TIMESTAMP(timezone=True),
    },
)


class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}  # noqa: RUF012
    registry = mapper_registry


@declarative_mixin
class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        sort_order=-100,
    )


@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=sa.text("timezone('utc', current_timestamp)"),
        sort_order=-99,  # noqa:WPS432
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=sa.text("timezone('utc', current_timestamp)"),
        onupdate=sa.text("timezone('utc', current_timestamp)"),
        sort_order=-98,  # noqa:WPS432
    )
