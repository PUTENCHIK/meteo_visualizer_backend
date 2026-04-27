from src.utils.exceptions.code.exception_code import ExceptionCode as ExceptionCode
from src.utils.exceptions.core.app import (
    RedisClientUnavailableException as RedisClientUnavailableException,
)
from src.utils.exceptions.core.auth import (
    InvalidAccessTokenException as InvalidAccessTokenException,
    InvalidPasswordException as InvalidPasswordException,
    InvalidRefreshTokenException as InvalidRefreshTokenException,
    InvalidTokenTypeException as InvalidTokenTypeException,
    LoginAlreadyUsesException as LoginAlreadyUsesException,
    PermissionDeniedException as PermissionDeniedException,
    RoleNotSetException as RoleNotSetException,
    TokenBlockedException as TokenBlockedException,
    TokenExpiredException as TokenExpiredException,
    TokenMissingException as TokenMissingException,
)
from src.utils.exceptions.core.base import (
    AppException as AppException,
    BadRequestException as BadRequestException,
    ConflictException as ConflictException,
    ForbiddenException as ForbiddenException,
    NotFoundException as NotFoundException,
    UnauthorizedException as UnauthorizedException,
)
from src.utils.exceptions.core.complexes import (
    ComplexHasNoAddressException as ComplexHasNoAddressException,
    ComplexNotDeletedException as ComplexNotDeletedException,
    ComplexNotFoundException as ComplexNotFoundException,
)
from src.utils.exceptions.core.mast_configs import (
    MastConfigHasActiveMastsException as MastConfigHasActiveMastsException,
    MastConfigNotDeletedException as MastConfigNotDeletedException,
    MastConfigNotFoundException as MastConfigNotFoundException,
    MastConfigTooLowException as MastConfigTooLowException,
)
from src.utils.exceptions.core.mast_yards import (
    InvalidMastYardHeightException as InvalidMastYardHeightException,
    MastYardAlreadyExistsException as MastYardAlreadyExistsException,
    MastYardNotFoundException as MastYardNotFoundException,
)
from src.utils.exceptions.core.masts import (
    MastHasSamePrefixException as MastHasSamePrefixException,
    MastNotFoundException as MastNotFoundException,
)
from src.utils.exceptions.core.measure_aliases import (
    MeasureAliasAlreadyExistsException as MeasureAliasAlreadyExistsException,
    MeasureAliasNotFoundException as MeasureAliasNotFoundException,
)
from src.utils.exceptions.core.measure_colors import (
    MeasureColorAlreadyExistsException as MeasureColorAlreadyExistsException,
    MeasureColorNotFoundException as MeasureColorNotFoundException,
)
from src.utils.exceptions.core.measures import (
    InvalidMeasureScaleException as InvalidMeasureScaleException,
    MeasureNotDeletedException as MeasureNotDeletedException,
    MeasureNotFoundException as MeasureNotFoundException,
)
from src.utils.exceptions.core.permissions import (
    PermissionNameAlreadyExistsException as PermissionNameAlreadyExistsException,
    PermissionNotDeletedException as PermissionNotDeletedException,
    PermissionNotFoundException as PermissionNotFoundException,
)
from src.utils.exceptions.core.roles import (
    RoleHasChildrenException as RoleHasChildrenException,
    RoleHasUsersException as RoleHasUsersException,
    RoleNameAlreadyExistsException as RoleNameAlreadyExistsException,
    RoleNotDeletedException as RoleNotDeletedException,
    RoleNotFoundException as RoleNotFoundException,
    RoleParentCantBeSameException as RoleParentCantBeSameException,
    RoleParentCircularException as RoleParentCircularException,
)
from src.utils.exceptions.core.users import (
    ImpossibleDeleteSelfException as ImpossibleDeleteSelfException,
    UserNotDeletedException as UserNotDeletedException,
    UserNotFoundException as UserNotFoundException,
)
