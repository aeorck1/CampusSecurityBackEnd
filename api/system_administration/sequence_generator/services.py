from django.core.cache import cache
from django.db import transaction

from appdata.models.sequence_generator import SequenceGenerator


class SequenceGeneratorService:
    CACHE_TIMEOUT = 3600
    CACHE_PREFIX = "seq_gen:"

    @classmethod
    def _cache_key(cls, sequence_id: str) -> str:
        return f"{cls.CACHE_PREFIX}{sequence_id}"

    @classmethod
    def next_val(cls, sequence_id: str) -> int:
        sequence_id = cls._escape(sequence_id)

        cached = cache.get(cls._cache_key(sequence_id))
        if cached and cached > 0:
            return cls._upsert(sequence_id, cached + 1)

        with transaction.atomic():
            obj, _ = SequenceGenerator.objects.select_for_update().get_or_create(
                sequence_id=sequence_id,
                defaults={"curr_val": 0},
            )
            obj.curr_val = (obj.curr_val or 0) + 1
            obj.save()
            cls._cache_set(sequence_id, obj.curr_val)
            return obj.curr_val

    @classmethod
    def curr_val_or_zero(cls, sequence_id: str) -> int:
        sequence_id = cls._escape(sequence_id)

        cached = cache.get(cls._cache_key(sequence_id))
        if cached is not None:
            return cached

        try:
            obj = SequenceGenerator.objects.get(sequence_id=sequence_id)
            cls._cache_set(sequence_id, obj.curr_val)
            return obj.curr_val
        except SequenceGenerator.DoesNotExist:
            return 0

    @classmethod
    def clear(cls):
        for key in cache.iter_keys(cls.CACHE_PREFIX + "*"):
            cache.delete(key)

    @classmethod
    def _upsert(cls, sequence_id: str, value: int) -> int:
        SequenceGenerator.objects.update_or_create(
            sequence_id=sequence_id,
            defaults={"curr_val": value}
        )
        cls._cache_set(sequence_id, value)
        return value

    @classmethod
    def _escape(cls, value: str) -> str:
        return value.replace("'", "''")

    @classmethod
    def _cache_set(cls, sequence_id: str, value: int):
        cache.set(cls._cache_key(sequence_id), value, timeout=cls.CACHE_TIMEOUT)