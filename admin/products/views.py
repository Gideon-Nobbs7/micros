from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status 
from .models import Fare
from .serializers import FareSerializer
# Create your views here.



class ProductViewset(viewsets.ViewSet):
    def list(self, request):
        fares = Fare.objects.all()
        serializer = FareSerializer(fares, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = FareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        fare = Fare.objects.get(id=pk)
        fare.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
