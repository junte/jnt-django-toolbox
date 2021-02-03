from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Aggregate, Func, IntegerField, Subquery, Value


class SQCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"  # noqa: WPS323
    output_field = models.IntegerField()
