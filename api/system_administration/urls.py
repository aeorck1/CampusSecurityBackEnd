from django.urls import path, include

from api.system_administration.user.views import UserListAPIView

urlpatterns = [
    path('auth/', include('api.system_administration.auth.urls')),
    path('users/', include('api.system_administration.user.urls')),
]