# -*- coding: utf8 -*-
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent

Page.register_extensions(
    'feincms.module.page.extensions.sites',
)

Page.register_templates({
    'title': u'Базовый шаблон',
    'path': 'cms_standard.html',
    'regions': (
        ('main', u'Страница'),
    ),
})
Page.register_templates({
    'title': u'Главная страница',
    'path': 'cms_index.html',
    'regions': (
        ('main', u'Страница'),
    ),
})

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', u'Без масштабирования'),
))
Page.register_with_reversion()
