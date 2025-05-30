from django.db import models


class SequenceGenerator(models.Model):
    sequence_id = models.CharField(max_length=255, primary_key=True)
    curr_val = models.BigIntegerField(null=False, blank=False)

    def __str__(self):
        return f"SequenceGenerator(sequence_id='{self.sequence_id}', curr_val={self.curr_val})"