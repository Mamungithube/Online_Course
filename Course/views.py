from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import Http404
from . import models, serializers

class CourseViewset(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Catagory__name']  # Search by related category name
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            course = self.get_object()
        except Http404:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(course)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            course = self.get_object()
        except Http404:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            course = self.get_object()
        except Http404:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response({"message": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

    

class CourseDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Course.objects.get(pk=pk)
        except models.Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        flower = self.get_object(pk)
        serializer = serializers.CourseSerializer(flower)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        flower = self.get_object(pk)
        serializer = serializers.CourseSerializer(flower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        flower = self.get_object(pk)
        flower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class EnrolledCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = models.Enrollment.objects.filter(user=request.user)
        serializer = serializers.EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    def post(self, request):
        # Handle course enrollment (example, you may need additional logic for validation)
        course_id = request.data.get('course')
        print(course_id)
        if not course_id:
            return Response({'detail': 'Course ID is required.'}, status=400)
        
        try:
            course = models.Course.objects.get(id=course_id)
            enrollment = models.Enrollment.objects.create(user=request.user, course=course)
            serializer = serializers.EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=201)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=404)