from rest_framework import serializers
from . import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)  # Nested course data

    class Meta:
        model = models.Enrollment
        fields = ['id', 'course', 'enrolled_at']