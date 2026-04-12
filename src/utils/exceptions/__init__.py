from src.utils.exceptions.base import (
    AppException as AppException,
    NotFoundException as NotFoundException,
    BadRequestException as BadRequestException,
    ConflictException as ConflictException,
    ForbiddenException as ForbiddenException,
    UnauthorizedException as UnauthorizedException,
)

from src.utils.exceptions.auth import (
    InvalidPasswordException as InvalidPasswordException,
    LoginAlreadyUsesException as LoginAlreadyUsesException,
    UserNotFoundException as UserNotFoundException,
)


from src.utils.exceptions.roles import (
    RoleNameAlreadyExistsException as RoleNameAlreadyExistsException,
    RoleNotDeletedException as RoleNotDeletedException,
    RoleNotFoundException as RoleNotFoundException,
    RoleParentCantBeSameException as RoleParentCantBeSameException,
    RoleHasChildrenException as RoleHasChildrenException,
    RoleHasUsersException as RoleHasUsersException,
)

from src.utils.exceptions.permissions import (
    PermissionNameAlreadyExistsException as PermissionNameAlreadyExistsException,
    PermissionNotFoundException as PermissionNotFoundException,
    PermissionNotDeletedException as PermissionNotDeletedException,
)