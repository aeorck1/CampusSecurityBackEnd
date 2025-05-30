from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.chat.comment.serializers import CommentAddSerializer, CommentListSerializer, CommentUpdateSerializer
from api.chat.comment.services import CommentService


@extend_schema_view(
    post=extend_schema(summary='Add comment (chat) on an object.',
                       description='Add comment (chat) on an object.',
                       tags=['Chat'])
)
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentAddSerializer
    permission_classes = (IsAuthenticated, )


@extend_schema_view(
    get=extend_schema(summary='Retrieve all comments (chats) on an object.',
                      description='Retrieve all comments (chats) on an object.',
                      tags=['Chat'])
)
class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CommentService.get_object_comments(
            object_type=self.kwargs['object_type'],
            object_id=self.kwargs['object_id'],
            user=self.request.user
        )


@extend_schema_view(
    get=extend_schema(summary='Retrieve a user\'s comment.',
                      description='Retrieve a user\'s comment.',
                      tags=['Chat']),
    patch=extend_schema(summary='Update a user\'s comment.',
                        description='Update a user\'s comment.',
                        tags=['Chat'])
)
class CommentSingleAPIView(RetrieveUpdateAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'patch', )

    def get_object(self):
        return CommentService.get_user_comment(comment_id=self.kwargs['id'], user=self.request.user)


@extend_schema_view(
    get=extend_schema(summary='Retrieve a comment.',
                      description='Retrieve a comment.',
                      tags=['Chat'])
)
class CommentRetrieveAPIView(RetrieveAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return CommentService.get_comment(comment_id=self.kwargs['id'])