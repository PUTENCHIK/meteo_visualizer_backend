from uuid import UUID

from src.utils.exceptions.core.base import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class RoleNameAlreadyExistsException(ConflictException):
    def __init__(self, name: str, is_deleted: bool):
        super().__init__(
            f"Роль '{name}' уже существует{' (мягко удалена)' if is_deleted else ''}"
        )


class RoleNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Роль ({id_.hex[:8]}) не найдена")


class RoleParentCantBeSameException(BadRequestException):
    def __init__(self):
        super().__init__("Роль не может иметь в качестве родителя саму себя")


class RoleNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Роль ({id_.hex[:8]}) не удалена")


class RoleHasChildrenException(ConflictException):
    def __init__(self, id_: UUID, count: int):
        super().__init__(
            f"Роль ({id_.hex[:8]}) имеет {count} потомков-ролей и не может быть удалена"
        )


class RoleHasUsersException(ConflictException):
    def __init__(self, id_: UUID, count: int):
        super().__init__(
            f"Роль ({id_.hex[:8]}) имеет {count} активных "
            f"пользователей и не может быть удалена"
        )
