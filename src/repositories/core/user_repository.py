from typing import Optional, override

from sqlalchemy import func
from sqlalchemy.orm import selectinload, with_loader_criteria

from src.models import AuditableModel, Complex, Mast, MastConfig, Role, User
from src.repositories.abstractions.auditable_repository import AuditableRepository


class UserRepository(AuditableRepository[User]):
    """
    Репозиторий сущностей пользователей
    """

    @override
    def __init__(self, session):
        super().__init__(User, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(User.role).selectinload(Role.parent),
            selectinload(User.role).selectinload(Role.children),
            selectinload(User.role).selectinload(Role.permissions),
            selectinload(User.complexes).selectinload(Complex.creator),
            selectinload(User.complexes)
            .selectinload(Complex.masts)
            .selectinload(Mast.config)
            .selectinload(MastConfig.yards),
            selectinload(User.created_complexes).selectinload(Complex.creator),
            selectinload(User.created_complexes)
            .selectinload(Complex.masts)
            .selectinload(Mast.config)
            .selectinload(MastConfig.yards),
            with_loader_criteria(
                AuditableModel,
                lambda cls: getattr(cls, "deleted_at", None) == None,
                include_aliases=True,
            ),
        )

    async def get_by_login(self, login: str) -> Optional[User]:
        statement = self._get_all_query().where(func.lower(User.login) == login.lower())
        result = await self.session.exec(statement)
        return result.one_or_none()
