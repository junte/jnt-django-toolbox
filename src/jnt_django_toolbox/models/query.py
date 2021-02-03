from django.db import models
from django.db.models import Subquery


class SQCount(Subquery):
    """Count items of subquery."""

    template = "(SELECT count(*) FROM (%(subquery)s) _count)"  # noqa: WPS323
    output_field = models.IntegerField()
