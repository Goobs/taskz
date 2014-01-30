from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def currency_icon(value):

    value = value.strip() if value else ''
    if value == 'RUB':
        return mark_safe('<i class="fa fa-rub"></i>')
    elif value == 'USD':
        return mark_safe('<i class="fa fa-usd"></i>')
    elif value == 'EUR':
        return mark_safe('<i class="fa fa-eur"></i>')
    return value


@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()
