from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() # amader router

router.register('list', views.TeacherViewset) # router er antena
router.register('Catagory', views.CatagorySerializer) # router er antena
router.register('reviews', views.ReviewViewset) # router er antena

urlpatterns = [
    path('', include(router.urls)),
]