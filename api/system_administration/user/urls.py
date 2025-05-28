from django.urls import path

from api.system_administration.user.views import UserListAPIView, StudentRegistrationView

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('students/register/', StudentRegistrationView.as_view(), name='student-register'),
]