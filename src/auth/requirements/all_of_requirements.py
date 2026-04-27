from src.auth.requirements.requirement_group import RequirementGroup


class AllOfRequirements(RequirementGroup):
    """
    Компоновщик требований. Требует все указанные разрешения пользователей
    """

    _func = all
