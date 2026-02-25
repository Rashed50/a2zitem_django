from django.contrib.auth.models import Group
from typing import Union, List

def user_in_group(user, groups: Union[str, List[str]]) -> bool:
    """
    Check if the given user belongs to one or more of the specified group(s).

    :param user: Django User object
    :param groups: Single group name or list of group names
    :return: True if user is in any of the given groups
    """
    if not user.is_authenticated:
        return False

    user_group_names = set(user.groups.values_list('name', flat=True))

    if isinstance(groups, str):
        return groups in user_group_names

    return bool(user_group_names.intersection(groups))
