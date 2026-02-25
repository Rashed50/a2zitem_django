from django import template

register = template.Library()

@register.simple_tag
def active_menu(request, url_names: str, class_name: str = "bg-white/10 dark:bg-white/5"):
    """
    Check if current URL matches any of the given URL names
    Usage: {% active_menu request 'app:url_name1,app:url_name2' %}
    """
    if not request or not request.resolver_match:
        return ""

    current_url_name = request.resolver_match.url_name
    current_app_name = request.resolver_match.app_name
    current_full_name = f"{current_app_name}:{current_url_name}" if current_app_name else current_url_name

    url_list = [name.strip() for name in url_names.split(',') if name.strip()]

    for url_pattern in url_list:
        if ':' in url_pattern:
            if url_pattern == current_full_name:
                return class_name
        else:
            if url_pattern == current_url_name:
                return class_name

    return ""

@register.simple_tag
def is_menu_open(request, url_names: str):
    """
    Check if menu should be open (for submenus)
    Usage: {% is_menu_open request 'app:url_name1,app:url_name2' %}
    """
    if not request or not request.resolver_match:
        return "false"

    current_url_name = request.resolver_match.url_name
    current_app_name = request.resolver_match.app_name
    current_full_name = f"{current_app_name}:{current_url_name}" if current_app_name else current_url_name

    url_list = [name.strip() for name in url_names.split(',') if name.strip()]

    for url_pattern in url_list:
        if ':' in url_pattern:
            if url_pattern == current_full_name:
                return "true"
        else:
            if url_pattern == current_url_name:
                return "true"

    return "false"