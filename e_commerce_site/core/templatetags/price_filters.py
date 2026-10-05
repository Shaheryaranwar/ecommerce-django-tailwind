from django import template

register = template.Library()


@register.filter
def pkr(value):
    """Format a Decimal as PKR, e.g. 245000 -> Rs 245,000"""
    try:
        return f"Rs {value:,.0f}"
    except (TypeError, ValueError):
        return value


@register.filter
def mul(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return value


@register.filter
def sub(value, arg):
    try:
        return value - arg
    except (TypeError, ValueError):
        return value
