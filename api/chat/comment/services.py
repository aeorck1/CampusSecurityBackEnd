import json
import re
from typing import Optional, Any, Tuple, Set

from django.core.serializers.json import DjangoJSONEncoder

from api.chat.comment_participant.services import CommentParticipantService
from api.system_administration.sequence_generator.services import SequenceGeneratorService
from appdata.models import Comment, User
from core.api.exceptions.exc import ResourceNotFoundException
from core.utils.object_utils import update_object_attributes


class CommentService:

    model = Comment

    MENTION_PATTERN = re.compile(r"\[([a-zA-Z0-9 _-]+)]\(([a-zA-Z0-9 _-]+)\)")

    @classmethod
    def add_comment(cls, validated_data: dict[str, Any]) -> Comment:

        parsed_comment, mentions = cls._parse_comment(validated_data['comment'])
        object_id = validated_data['object_id']
        validated_data['position'] = SequenceGeneratorService.next_val(object_id)
        parent_comment = validated_data.get('parent_comment')

        if parent_comment is not None:
            parent_comment_metadata = {
                "comment": parent_comment.comment,
                "created_by_user": parent_comment.created_by_user,
                "date_created": parent_comment.date_created,
                "position": parent_comment.position,
            }
            validated_data['parent_comment_metadata'] = json.dumps(parent_comment_metadata, cls=DjangoJSONEncoder)

        comment = cls.model.objects.create(**validated_data)

        CommentParticipantService.mark_comment_as_read(comment.object_type, comment.object_id, comment.comment_by,
                                                       comment.position)

        return comment

    @classmethod
    def update_comment(cls, instance: model, validated_data: dict[str, Any]) -> model:
        update_object_attributes(instance, validated_data)
        instance.save()
        return instance

    @classmethod
    def get_comment(cls, comment_id: str) -> Optional[Comment]:
        try:
            return cls.model.objects.get(id=comment_id)
        except cls.model.DoesNotExist:
            raise ResourceNotFoundException('Comment not found')

    @classmethod
    def get_user_comment(cls, comment_id: str, user: User):
        try:
            return cls.model.objects.get(id=comment_id, comment_by=user)
        except cls.model.DoesNotExist:
            raise ResourceNotFoundException('Comment not found')

    @classmethod
    def get_object_comments(cls, object_type: str, object_id: str, user: User = None):
        query_set = cls.model.objects.filter(object_type=object_type, object_id=object_id).order_by('position')

        if query_set.count() > 0 and user is not None:
            CommentParticipantService.mark_comment_as_read(object_type=object_type, object_id=object_id,
                                                       comment_position=query_set.last().position,
                                                       user=user)

        return query_set

    @classmethod
    def _parse_comment(cls, comment: str) -> Tuple[str, Set[str]]:
        user_ids = set()
        for match in cls.MENTION_PATTERN.finditer(comment):
            user_ids.add(match.group(2))
            comment = comment.replace(
                match.group(),
                f'<span class="comment_blue" data="{match.group(2)}">@{match.group(1)}</span>'
            )
        return comment, user_ids
