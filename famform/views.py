from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from .models import FamEstFormData 
from .serializers import FamEstFormDataNetSerializer 
from rest_framework.parsers import JSONParser

from rest_framework.response import Response
# Create your views here.

class FamEstFormDataViewSet(viewsets.ViewSet):
    seriazizer_class = FamEstFormDataNetSerializer

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = FamEstFormDataNetSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
