from django.urls import path

from api.chat.comment.views import CommentCreateAPIView, CommentListAPIView, CommentSingleAPIView, \
    CommentRetrieveAPIView

urlpatterns = [
    path('', CommentCreateAPIView.as_view(), name='comment-create'),
    path('objects/<str:object_type>/<str:object_id>/', CommentListAPIView.as_view(), name='comment-list'),
    path('<str:id>/users/', CommentSingleAPIView.as_view(), name='comment-single'),
    path('<str:id>/', CommentRetrieveAPIView.as_view(), name='comment-retrieve'),
]