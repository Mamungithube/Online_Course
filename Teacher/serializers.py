from rest_framework import serializers
from . import models

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    Catagory = serializers.StringRelatedField(many=True)
    course_title = serializers.StringRelatedField(source='Course.name', read_only=True)

    class Meta:
        model = models.Teacher
        fields = ['id', 'user', 'image', 'Catagory', 'Course', 'meet_link' , 'course_title']
class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catagory
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    course_title = serializers.CharField(source='Course.name', read_only=True)
    class Meta:
        model = models.Review
        fields = ['id', 'body', 'created', 'rating', 'reviewer', 'Course', 'reviewer_name', 'course_title']
    def get_reviewer_name(self, obj):
        return obj.reviewer.username  

    def get_course_name(self, obj):
        return obj.course.title