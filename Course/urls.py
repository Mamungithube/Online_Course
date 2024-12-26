from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
router = DefaultRouter() 

router.register('list', views.CourseViewset)
urlpatterns = [
    path('', include(router.urls)),
    path('Course/<int:pk>/', views.CourseDetail.as_view(), name='Course_Detail'),
    path('enrolled-courses/', views.EnrolledCoursesView.as_view(), name='enrolled-courses'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)