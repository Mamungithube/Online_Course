from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated


class CatagorySerializer(viewsets.ModelViewSet):
    queryset = models.Catagory.objects.all()
    serializer_class = serializers.CatagorySerializer
    
class TeacherViewset(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__email', 'Catagory__name']
    
class ReviewViewset(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer