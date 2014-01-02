from base import *

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'dugzb0gwyj!02$3wq)b)23bel5ai@0m4j=^l%ybsdvs_q=lb&l'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'base.db'),
    }
}
