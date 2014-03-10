# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class InlineEditView(APIView):
    model = None

    def post(self, request, **kwargs):
        _obj = get_object_or_404(self.model, pk=request.POST.get('pk'))
        field = request.POST.get('name')
        value = request.POST.get('value')
        setattr(_obj, field, value)
        try:
            _obj.full_clean()
        except ValidationError as e:
            return Response(e.error_dict, status=400)
        _obj.save()
        return Response({'status': 'OK'})
