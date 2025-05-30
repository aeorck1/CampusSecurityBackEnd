from dataclasses import dataclass

from django.utils import timezone

from api.system_administration.sequence_generator.services import SequenceGeneratorService
from appdata.models import User
from appdata.models import CommentParticipant
from core.constants.system_enums import ObjectType


@dataclass
class CommentCountMetadata:
    object_id: str
    object_type: ObjectType
    total_count: int
    last_count: int


class CommentParticipantService:

    model = CommentParticipant

    @classmethod
    def mark_comment_as_read(cls, object_type: ObjectType | str, object_id: str, user: User, comment_position: int):
        participant, created = cls.model.objects.get_or_create(
            object_type=object_type,
            object_id=object_id,
            user=user,
            defaults={
                "last_count": comment_position,
                "date_created": timezone.now(),
            }
        )
        if not created:
            participant.last_count = comment_position
            participant.save()

    @classmethod
    def get_user_comment_count(cls, object_type: ObjectType | str, object_id: str, user: User) -> CommentCountMetadata:

        total_count = SequenceGeneratorService.curr_val_or_zero(object_id)

        try:
            participant = cls.model.objects.get(object_type=object_type, object_id=object_id, user=user)
            last_count = participant.last_count
        except cls.model.DoesNotExist:
            last_count = 0

        return CommentCountMetadata(
            object_id=object_id,
            object_type=object_type,
            total_count=total_count,
            last_count=last_count,
        )
