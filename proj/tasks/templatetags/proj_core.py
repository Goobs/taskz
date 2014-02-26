import hashlib
from django import template
from django.utils.safestring import mark_safe
from sorl import thumbnail
from proj.core.message.models import Message

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


@register.assignment_tag
def user_dialogs(user):
    return Message.objects.last(user)[:10]


@register.assignment_tag
def user_notifications(user):
    return Message.objects.filter(recepient=user, read=False)


@register.simple_tag
def avatar(user, width=80):
    if user.avatar:
        thumb = thumbnail.get_thumbnail(user.avatar, '%sx%s' % (width, width), crop='center', quality=99)
        return thumb.url
    ghash = hashlib.md5(user.email.lower().strip()).hexdigest()
    return 'http://gravatar.com/avatar/%s?d=identicon&s=%s' % (ghash, width)


@register.simple_tag
def community_image(community, width=80):
    if community.image:
        thumb = thumbnail.get_thumbnail(community.image, '%sx%s' % (width, width), crop='center', quality=99)
        return thumb.url
    return 'http://dummyimage.com/%sx%s' % (width, width)
