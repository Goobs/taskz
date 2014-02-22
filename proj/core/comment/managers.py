# -*- coding: utf-8 -*-

from django.db import models


class CommentManager(models.Manager):

    def comment_feed(self):
        return self.order_by('date')
