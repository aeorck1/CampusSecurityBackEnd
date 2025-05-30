from django.urls import path

from api.system_administration.user.views import UserListAPIView, StudentRegistrationView, UserProfileUpdateView

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('students/register/', StudentRegistrationView.as_view(), name='student-register'),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
]