from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from news.models import Post
from news.serializers import PostListingSerializer, PostSerializer
from settings import CACHE_TTL


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = PostListingSerializer
    ordering_fields = ['title', 'created', ]
    filterset_fields = ['title', ]
    ordering = ['-created']  # default

    # @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, slug):
        # this is a crutch
        post = get_object_or_404(Post, slug=slug)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super(PostView, self).list(request, *args, **kwargs)
