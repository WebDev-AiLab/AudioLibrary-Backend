from botocore.serialize import QuerySerializer
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework import status, permissions
from rest_framework.templatetags import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, DestroyAPIView

import settings
from tools.location import get_location
from tools.visitor import get_visitor_ip_address
from .models import Guest, User
from interactions.models import Vote, Play
from .serializers import UserPrivateSerializer, CreateGuestSerializer, UserChangePasswordSerializer, \
    UserDeactivateSerializer, UserRegistrationSerializer, UserVerificationSerializer, UserRestorePasswordSerializer, \
    CreateApplicationSerializer, UserAuthGoogleSerializer
from tracks.serializers import TrackListingSerializer
from tracks.models import Track
from tools.string import generate_random_string
from tools.pagination import StandardResultsSetPagination
from django.db.models.aggregates import Max
from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from settings.cache import CACHE_TTL

import json


class AccountsPrivateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # manually check permissions
        if not self.has_permissions(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        queryset = User.objects.get(id=request.user.id)
        serializer = UserPrivateSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    # i'm not sure if this is right, but for now i'm doing manual permission check
    def has_permissions(self, request):
        if request.user and request.user.is_authenticated:
            return True
        else:
            return False


class GuestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # if user already authorized do nothing
        if not request.user.is_anonymous:
            return Response(status=status.HTTP_409_CONFLICT)

        # just create it and generate token
        user = User.objects.create(
            username=f"Anonymous_{generate_random_string(32)}",
            ip=get_visitor_ip_address(request),
            is_guest=True,
            is_active=True  # guests are always active
        )

        ####
        ## i'm not really sure that i have to do it manually...
        ## https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html
        ####

        token = RefreshToken.for_user(user)
        return Response({
            'id': user.id,
            'access': str(token.access_token),
            'refresh': str(token)
        }, status=status.HTTP_201_CREATED)


class BeaconView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = CreateGuestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(True)
        serializer.validated_data['ip'] = get_visitor_ip_address(request)

        # get location info
        location = get_location(serializer.validated_data['ip'])
        serializer.validated_data['city'] = location['city']
        serializer.validated_data['country'] = location['country']
        serializer.validated_data['region'] = location['region']
        serializer.validated_data['timezone'] = location['timezone']
        serializer.validated_data['utc_offset'] = location['utc_offset']
        serializer.validated_data['latitude'] = location['latitude']
        serializer.validated_data['longitude'] = location['longitude']
        serializer.validated_data['ipv'] = location['version']

        serializer.update(instance=user, validated_data=serializer.validated_data)
        return Response('beep', status=status.HTTP_200_OK)


class StatisticsView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 1))  # 1 minute
    def get(self, request):
        ten_minutes = timezone.now() - timedelta(minutes=1)
        queryset = User.objects.filter(last_seen__gte=ten_minutes)

        count_overall = queryset.count()
        count_guests = queryset.filter(is_guest=True).count()
        count_users = count_overall - count_guests

        return Response({
            'count_overall': count_overall,
            'count_users': count_users,
            'count_guests': count_guests
        })


class AccountPrivateTracksView(ListAPIView, DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrackListingSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Track.objects.all().filter(celery_upload_status=3)

    def list(self, request):

        subject = request.query_params.get('subject')
        if subject == 'plays':
            queryset = self.queryset.filter(plays__user=request.user).annotate(max=Max('plays__id')).order_by('-max')

        elif subject == 'likes':
            queryset = self.queryset.filter(votes__user=request.user).order_by('-votes__created')

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TrackListingSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = TrackListingSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        subject = request.query_params.get('subject')

        if subject == 'plays':
            Play.objects.filter(user=request.user).delete()

        elif subject == 'likes':
            Vote.objects.filter(user=request.user).delete()

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAuthGoogle(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(request=UserAuthGoogleSerializer)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_guest:
            return Response(
                status=status.HTTP_400_BAD_REQUEST)
        if settings.SECRET_KEY_AUTH != request.data.get('secret_key'):
            return Response(
                status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserAuthGoogleSerializer(data=request.data)
        serializer.is_valid(True)

        try:
            if user := get_object_or_404(User, email=request.data.get('email')):
                token = RefreshToken.for_user(user)
                return Response({
                    'id': user.id,
                    'access': str(token.access_token),
                    'refresh': str(token)
                }, status=status.HTTP_200_OK)

        except Http404:
            try:
                user = serializer.create(serializer.validated_data)
                token = RefreshToken.for_user(user)
                return Response({
                    'id': user.id,
                    'access': str(token.access_token),
                    'refresh': str(token)
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response('Not a unique name', status=status.HTTP_400_BAD_REQUEST)




class UserRegistrationView(APIView):
    # default permissions
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # manually check permissions
        if request.user.is_authenticated and not request.user.is_guest:
            return Response(
                status=status.HTTP_400_BAD_REQUEST)  # we do not allow authorized user to register, that doesn't make sense
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(True)  # put raise exception, so this bad boy can do everything by itself
        user = serializer.create(serializer.validated_data)

        # generate JWT Manually, so user can be authorized without further actions
        token = RefreshToken.for_user(user)
        return Response({
            # 'access': str(token.access_token),
            # 'refresh': str(token)
        }, status=status.HTTP_201_CREATED)





class UserVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserVerificationSerializer(data=request.data)
        serializer.is_valid(True)
        result = serializer.verify(validated_data=serializer.validated_data)
        if not result:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UserRestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRestorePasswordSerializer(data=request.data)
        serializer.is_valid(True)
        result = serializer.restore(validated_data=serializer.validated_data)
        if not result:
            # todo notify user what went wrong
            # for now the only thing that can go wrong is when user doesn't exist
            # but who knows what will be in future
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UserDeactivateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserDeactivateSerializer(data=request.data)
        serializer.is_valid(True)
        result = serializer.deactivate(validated_data=serializer.validated_data)
        if not result:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(True)
        result = serializer.change_password(validated_data=serializer.validated_data)
        # todo notify user that password have changed
        if not result:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class CreateApplicationView(CreateAPIView):
    serializer_class = CreateApplicationSerializer
    permission_classes = (permissions.AllowAny,)
