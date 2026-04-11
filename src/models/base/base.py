from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
