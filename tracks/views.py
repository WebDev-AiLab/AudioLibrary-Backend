from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import CreateTrackSerializer, TrackListingSerializer, CreatePlaySerializer, StyleSerializer, \
    ArtistSerializer, CreateLikeSerializer, LabelSerializer, CommentSerializer, CreateCommentSerializer, \
    SubmissionSerializer, RatingSerializer, CreateCommentArtistSerializer
from .models import Track, Style, Artist, Label, Submission, Rating
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from interactions.models import Play, Vote, Comment
from tools.visitor import get_visitor_ip_address
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from tools.pagination import StandardResultsSetPagination
from datetime import datetime, timedelta
from django.db.models import Count, Q

from rest_framework.pagination import LimitOffsetPagination

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from tools.validators import grecaptcha_validator
from rest_framework.serializers import ValidationError

from settings.cache import CACHE_TTL


class TrackView(ModelViewSet):
    permission_classes = [permissions.AllowAny]  # temporary, todo make normal permissions when ready
    queryset = Track.objects.all() \
        .filter(title__isnull=False, original_artist__isnull=False, celery_upload_status=3) \
        .prefetch_related('artist')

    serializer_class = TrackListingSerializer

    # filtering and ordering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['title', 'created', 'votes_count', 'comments', 'plays_count']
    filterset_fields = ['artist', 'label', 'album', 'show_new_releases']
    search_fields = ['title']
    ordering = ['created']  # default
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        # if not request.user or not request.user.is_authenticated or not request.user.is_staff:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = CreateTrackSerializer(data=request.data, context={'request': request})
        serializer.is_valid(True)
        serializer.validated_data['original_file_name'] = request.FILES['file'].name
        result = serializer.create(validated_data=serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED, data={
            'id': result.id
        })

    # @method_decorator(vary_on_headers("Authorization", ))
    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ordering = request.query_params.get('ordering')
        print(request.query_params)

        # trending
        # the logic is simple - order tracks by number of likes in the last day
        if ordering == 'trending':
            one_day = datetime.today() - timedelta(days=7)
            queryset = queryset.annotate(plays_trend=Count('plays', filter=Q(plays__created__gte=one_day)),
                                         plays_count_real=Count('plays')).order_by('-plays_trend', '-plays_count_real')

        if ordering == 'hottest':
            one_day = datetime.today() - timedelta(days=1)
            queryset = queryset.annotate(votes_trend=Count('votes', filter=Q(votes__created__gte=one_day)),
                                         plays_count_real=Count('plays')).order_by('-votes_trend',
                                                                                   '-plays_count_real')

        # temporary
        # todo pass this from frontend
        latest = request.query_params.get('latest')
        if latest:
            print('latest')
            queryset = queryset.filter(created__gte=(datetime.today() - timedelta(days=30)))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrackListingSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = TrackListingSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

    # @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, pk, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            track = queryset.get(pk=pk)

            serializer = TrackListingSerializer(track, context={'request': request})
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # @method_decorator(cache_page(CACHE_TTL))
    def retrieve_slug(self, request, slug, *args, **kwargs):
        # this is a crutch
        track = get_object_or_404(Track, slug=slug)
        serializer = TrackListingSerializer(track, context={'request': request})
        return Response(serializer.data)


# todo move this to interactions app
class PlayView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Play.objects.all()

    def post(self, request, pk):
        serializer = CreatePlaySerializer(
            data={'track': pk, 'user': request.user.id, 'ip': get_visitor_ip_address(request)})
        serializer.is_valid(True)
        serializer.create(validated_data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):

        # check permissions
        print(request.user)
        if not request.user or not request.user.is_authenticated or not request.user.is_staff:
            pass
            # return Response(status=status.HTTP_401_UNAUTHORIZED)

        track = get_object_or_404(Track, pk=pk)

        try:
            like = self.queryset.filter(track=pk)
            like.delete()
        except ObjectDoesNotExist:
            pass

        # todo move this to play or play signals or something
        track.evaluate_counts()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    pagination_class = StandardResultsSetPagination

    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, pk, *args, **kwargs):
        queryset = self.queryset.filter(track=pk).order_by('-created')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CommentSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

    def post(self, request, pk):
        data = request.data
        data['track'] = pk
        data['type'] = 'track'
        data['user'] = request.user.id
        serializer = CreateCommentSerializer(data=data)
        serializer.is_valid(True)
        serializer.create(validated_data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk, comment_pk):
        # just do it manually, because it is very simple
        # it will raise error if captcha is invalid, so there's nothing to do
        grecaptcha_validator(request)(request.query_params.get('token'))
        get_object_or_404(Comment, id=comment_pk, track=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentArtistView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    pagination_class = StandardResultsSetPagination

    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, pk, *args, **kwargs):
        queryset = self.queryset.filter(artist=pk).order_by('-created')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CommentSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

    def post(self, request, pk):
        data = request.data
        data['artist'] = pk
        data['user'] = request.user.id
        data['type'] = 'artist'
        serializer = CreateCommentArtistSerializer(data=data)
        serializer.is_valid(True)
        serializer.create(validated_data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk, comment_pk):
        # just do it manually, because it is very simple
        # it will raise error if captcha is invalid, so there's nothing to do
        grecaptcha_validator(request)(request.query_params.get('token'))
        get_object_or_404(Comment, id=comment_pk, artist=pk, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vote.objects.all()

    def post(self, request, pk):
        try:
            like = self.queryset.get(track=pk, user=request.user.id)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            serializer = CreateLikeSerializer(
                data={'track': pk, 'user': request.user.id, 'token': request.data.get('token')})
            serializer.is_valid(True)
            serializer.create(validated_data=serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)

    # def delete(self, request, pk):
    #     try:
    #         like = self.queryset.get(video=pk, user=request.user.id)
    #         like.delete()
    #     except ObjectDoesNotExist:
    #         pass
    #
    #     # return anyway
    #     # initially i threw an error, but there's no need
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class LabelView(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    serializer_class = LabelSerializer

    queryset = Label.objects.all()

    ordering_fields = ['name', 'created', ]
    ordering = ['name']  # default

    # @method_decorator(cache_page(CACHE_TTL))
    # def get(self, *args, **kwargs):
    #     return super().get(*args, **kwargs)

    # @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, slug, *args, **kwargs):
        label = get_object_or_404(Label, slug=slug)
        serializer = LabelSerializer(label, context={'request': request})
        return Response(serializer.data)


class ArtistView(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created', 'name']
    pagination_class = StandardResultsSetPagination
    serializer_class = ArtistSerializer

    queryset = Artist.objects.filter(hide=False, visible=True) \
        .prefetch_related('artist_images')

    # def get_queryset(self):
    #     return self.queryset

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_headers("Authorization", ))
    def list(self, request, *args, **kwargs):

        ordering = request.query_params.get('ordering')
        one_day = datetime.today() - timedelta(days=7)

        if ordering == 'trending':

            # order by number of plays in datetime span
            self.queryset = self.queryset.annotate(
                plays_trend=Count('tracks__plays', filter=Q(tracks__plays__created__gte=one_day))) \
                .order_by('-plays_trend')

        elif ordering == 'featured':

            # almost the same that with the track
            self.queryset = self.queryset.annotate(
                votes_trend=Count('tracks__votes', filter=Q(tracks__votes__created__gte=one_day)),
                plays_count_real=Count('tracks__plays')).order_by('-votes_trend', '-plays_count_real')

        elif ordering == 'my' and not request.user.is_anonymous:

            # order by number of playing by current user
            # todo move this to account, please
            self.queryset = self.queryset.annotate(
                plays_trend=Count('tracks__plays', filter=Q(tracks__plays__user=request.user))) \
                .order_by('-plays_trend')

        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, slug, *args, **kwargs):
        artist = get_object_or_404(Artist, slug=slug, visible=True)
        serializer = ArtistSerializer(artist, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            artist_name = request.data.get('artist').strip()
            obj, created = Artist.objects.get_or_create(
                name=artist_name
            )
            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                print(f"{artist_name} already exists")
        except Exception as e:
            print(e)
        return Response(status=status.HTTP_200_OK)

class StylesListing(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = StyleSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['genre']
    queryset = Style.objects.all()

    # @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SubmissionView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class RatingListing(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering = ['-rating']

    # @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)