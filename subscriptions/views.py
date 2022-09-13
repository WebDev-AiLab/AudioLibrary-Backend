from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import CreateSubscriberSerializer
from .models import Subscriber
from rest_framework.response import Response


# Create your views here.
class SubscriberView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateSubscriberSerializer(data=request.data)
        serializer.is_valid(True)

        # weird stuff
        obj, created = Subscriber.objects.get_or_create(email=request.data.get('email'))
        if created:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_200_OK)
