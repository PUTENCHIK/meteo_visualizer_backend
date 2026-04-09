from typing import Optional
from uuid import UUID

from src.models.base.base import Base


class ManyToManyModel(Base):
    creator_id: Optional[UUID]
