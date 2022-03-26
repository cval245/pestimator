from os.path import exists

from django.conf import settings
from rest_framework import permissions, renderers, viewsets
# Create your views here.
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from rest_framework.response import Response
from lawfirm.models import LawFirm
from lawfirm.serializers import LawFirmSerializer
from user.accesspolicies import GetOnlyPolicy


class LawFirmViewSet(viewsets.ModelViewSet):
    serializer_class = LawFirmSerializer
    permission_classes = [GetOnlyPolicy]

    def get_queryset(self):
        queryset = LawFirm.objects.all()
        slug = self.request.query_params.get('nameslug')
        if slug is not None:
            queryset = LawFirm.objects.filter(slug=slug)

        return queryset


class WebpRenderer(renderers.BaseRenderer):
    media_type = 'image/webp'
    format = 'webp'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


@api_view(['GET'])
@renderer_classes([WebpRenderer])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def get_law_firm_image(request, image_location):
    try:
        image = open(settings.STATIC_ROOT + '/law-firm-images/' + image_location + '.webp', "br")
    except FileNotFoundError:
        image = open(settings.STATIC_ROOT + '/law-firm-images/empty-image.webp', 'br')
    return Response(image)
