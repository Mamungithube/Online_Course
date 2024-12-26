from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import UserRegistrationAPIView, UserProfileView, ChangePasswordViewSet,UserLoginApiView,UserLogoutApiView,RegisteredUsersCount,activate,IsAdminStatusAPIView
router = DefaultRouter()

router.register('list', views.StudentViewset)
router.register(r'pass_cng', ChangePasswordViewSet, basename='pass_cng')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    # path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('active/<uid64>/<token>', activate, name='activate'),
    # path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('registered-users-count/', RegisteredUsersCount.as_view(), name='registered_users_count'),
    path('admins/', IsAdminStatusAPIView.as_view(), name='admins')
]