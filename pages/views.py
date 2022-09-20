from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Page
from .serializers import PageSerializer, PageLightSerializer, PageParam
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from settings.cache import CACHE_TTL


# Create your views here.
class PageView(ModelViewSet):
    queryset = Page.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = PageSerializer
    ordering_fields = ['title', 'created', ]
    filterset_fields = ['title', 'section', 'type', 'page']
    ordering = ['section', 'order', '-created']  # default

    @extend_schema(parameters=[PageParam])
    def retrieve(self, request):
        # this is a crutch
        url = request.query_params.get('url')
        page = get_object_or_404(Page, url_mask=url)
        serializer = PageSerializer(page, context={'request': request})
        return Response(serializer.data)

    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super(PageView, self).list(request, *args, **kwargs)
