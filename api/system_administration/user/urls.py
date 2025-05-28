from django.urls import path

from api.system_administration.user.views import UserListAPIView

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
]