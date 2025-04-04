import random

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Fare, User
from .producer import publish_to_queue
from .serializers import FareSerializer

# Create your views here.


class FareViewset(viewsets.ViewSet):
    def list(self, request):
        fares = Fare.objects.all()
        serializer = FareSerializer(fares, many=True)
        publish_to_queue("fare_list", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = FareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish_to_queue("new_fare", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        fare = Fare.objects.get(id=pk)
        serializer = FareSerializer(fare)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        fare = Fare.objects.get(id=pk)
        serializer = FareSerializer(instance=fare, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish_to_queue("fare_updated", serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        fare = Fare.objects.get(id=pk)
        publish_to_queue("fare_deleted", pk)
        fare.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({"id": user.id})
