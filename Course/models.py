from django.db import models
from django.conf import settings
class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    # image = models.ImageField(upload_to="Course/images/" , blank=True, null=True)
    image = models.CharField(max_length=100 , default='')
    month = models.IntegerField()
    Course_fee = models.IntegerField()
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"

