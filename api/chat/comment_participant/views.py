from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from api.chat.comment_participant.serializers import CommentCountSerializer
from api.chat.comment_participant.services import CommentParticipantService


@extend_schema_view(
    get=extend_schema(summary='Retrieve a comment count metadata.',
                      description='Retrieve a comment count metadata for an object for a user.',
                      tags=['Chat'])
)
class CommentCountMetadataRetrieveAPIView(RetrieveAPIView):
    serializer_class = CommentCountSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return CommentParticipantService.get_user_comment_count(
            object_type=self.kwargs['object_type'],
            object_id=self.kwargs['object_id'],
            user=self.request.user
        )
