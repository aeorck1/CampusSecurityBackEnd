from django.urls import path

from api.chat.comment_participant.views import CommentCountMetadataRetrieveAPIView

urlpatterns = [
    path('comments/objects/<str:object_type>/<str:object_id>/count/', CommentCountMetadataRetrieveAPIView.as_view(), name='comment-count-metadata'),
]