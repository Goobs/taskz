from django.contrib.auth.decorators import *



def unauthorized_only(view_func):
    """
    Allows only unauthorized access, otherwise redirecting to root.
    """
    def is_anonymous(user):
        return user.is_anonymous()

    login_url = '/feed'

    return user_passes_test(is_anonymous, login_url=login_url, redirect_field_name=None)(view_func)

