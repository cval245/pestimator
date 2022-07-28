import os
import uuid as uuid
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.functions import Substr
from django.http import HttpResponseForbidden
from django.utils.text import slugify
from rest_framework import permissions, renderers, status, viewsets
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from lawfirm.models import LawFirm, LawFirmFees
from lawfirm.serializers import LawFirmFeesSerializer, LawFirmSerializer
from user.accesspolicies import AllGetStaffOnlyPost, GetOnlyPolicy, LawFirmPostAndGetAccess, StaffOnlyAccess


class LawFirmLawyerEditorViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmSerializer
    permission_classes = [LawFirmPostAndGetAccess]

    def get_queryset(self):
        try:
            queryset = LawFirm.objects.get(id=self.request.user.lawfirm)
        except:
            queryset = LawFirm.objects.none()

        return queryset

    def update(self, request, *args, **kwargs):
        if LawFirm.objects.filter(user__in=request.user.id).exists():
            return super().update(request=request, args=args, kwargs=kwargs)
        else:
            return HttpResponseForbidden()


class LawFirmAdminViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        slug = self.request.query_params.get('nameslug')
        if slug is not None:
            queryset = LawFirm.objects.filter(slug=slug)
        else:
            queryset = LawFirm.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        slug = self.request.query_params.get('nameslug')
        if slug is not None:
            if LawFirm.objects.filter(slug=slug).exists() is False:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return super().list(request)

    def create(self, request, *args, **kwargs):
        new_request = request
        request.data['slug'] = slugify(request.data['name'])
        context = {'request': new_request}
        serializer = LawFirmSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # new_request = request
        request.data['slug'] = slugify(request.data['name'])
        return super().update(request=request, args=args, kwargs=kwargs)


class LawFirmViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmSerializer
    permission_classes = [GetOnlyPolicy]

    def get_queryset(self):
        queryset = LawFirm.objects.all()
        slug = self.request.query_params.get('nameslug')
        if slug is not None:
            queryset = LawFirm.objects.filter(slug=slug)

        return queryset


class LawFirmFeesViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmFeesSerializer
    permission_classes = [StaffOnlyAccess]

    def get_queryset(self):
        return LawFirmFees.objects.all()


class LawFirmFeesForLawyerViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmFeesSerializer
    permission_classes = [LawFirmPostAndGetAccess]

    def get_queryset(self):
        user = self.request.user
        return LawFirmFees.objects.filter(lawfirm__user=user)


class WebpRenderer(renderers.BaseRenderer):
    media_type = 'image/webp'
    format = 'webp'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


@api_view(['POST'])
@renderer_classes([WebpRenderer])
@permission_classes([AllGetStaffOnlyPost, LawFirmPostAndGetAccess])
def post_lawfirm_image(request, lawfirm_id):
    image = request.data['file']
    if LawFirm.objects.filter(id=lawfirm_id).exists():
        lawfirm = LawFirm.objects.get(id=lawfirm_id)
        lawfirm.image_location = image
        if isinstance(image, InMemoryUploadedFile):
            lawfirm.save()
        serializer = LawFirmSerializer(lawfirm)
        json = JSONRenderer().render(serializer.data)
        return Response(json)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
