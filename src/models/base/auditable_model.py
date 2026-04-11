from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlmodel import Field

from src.models.base.base import Base


class AuditableModel(Base):
    id: UUID = Field(primary_key=True, default_factory=uuid4, nullable=False)

    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        nullable=False,
    )

    deleted_at: Optional[datetime] = Field(
        sa_type=DateTime(timezone=True),
        default=None,
        index=True,
        nullable=True,
    )
