from django.urls import path

from api.system_administration.auth.views import ObtainTokenPairView, RefreshTokenView, VerifyTokenView, \
    PasswordResetRequestView, PasswordResetCompleteView

urlpatterns = [
    path('login/', ObtainTokenPairView.as_view(), name='obtain-token-pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('token/verify/', VerifyTokenView.as_view(), name='verify-token'),
    path("initiate-password-reset/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("complete-password-reset/", PasswordResetCompleteView.as_view(), name="password-reset-complete"),
]
