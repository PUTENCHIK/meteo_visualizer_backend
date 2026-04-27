from abc import ABC
from typing import Callable, Iterable, Set, Tuple, Union

from src.auth.enums import SystemPermission


class RequirementGroup(ABC):
    """
    Абстрактный компонтовщик требований к разрешениям пользователей
    """

    _func: Callable[[Iterable], bool]
    _requirements: Tuple[Union[SystemPermission, 'RequirementGroup']]

    @property
    def func(self) -> Callable[[Iterable], bool]:
        """
        Функция all или any
        """
        return self._func
    
    @property
    def requirements(self) -> Tuple[Union[SystemPermission, 'RequirementGroup']]:
        return self._requirements

    def __init__(self, *requirements: Union[SystemPermission, 'RequirementGroup']):
        super().__init__()
        self._requirements = requirements

    def __call__(
        self,
        user_perms: Set[str]
    ):
        result = list()
        for requirement in self.requirements:
            if isinstance(requirement, SystemPermission):
                result.append(requirement.value in user_perms)
            else:
                result.append(requirement(user_perms))

        return self.func(result)
    
    def __str__(self):
        func_names = {
            'all': 'все из',
            'any': 'одно из'
        }
        name = func_names[self.func.__name__]
        return f"{name} ({', '.join([str(r) for r in self.requirements])})"
