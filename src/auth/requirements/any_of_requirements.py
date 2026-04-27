from src.auth.requirements.requirement_group import RequirementGroup


class AnyOfRequirements(RequirementGroup):
    """
    Компоновщик требований. Требует любое из указанных разрешений пользователей
    """

    _func = any
