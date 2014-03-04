# -*- coding: utf-8 -*-

from proj.core.models import *
import uuid
from django.utils.crypto import get_random_string


def custom_user_create(request, ulogin_response):

    user = User.objects.create_user(email=uuid.uuid4().hex,
                password=get_random_string(10, '0123456789abcdefghijklmnopqrstuvwxyz'),
                full_name='')

    return user
