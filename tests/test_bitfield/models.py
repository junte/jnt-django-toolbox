# -*- coding: utf-8 -*-

from django.db import models

from jnt_django_toolbox.models.fields import BitField


class BitFieldTestModel(models.Model):
    """Model for testing bitfield."""

    flags = BitField(
        flags=("FLAG1", "FLAG2", "FLAG3", "FLAG4"),
        default=3,
        db_column="another_name",
    )


class CompositeBitFieldTestModel(models.Model):
    """Model for testing complex bitfields."""

    flags1 = BitField(flags=("FLAG1", "FLAG2", "FLAG3", "FLAG4"), default=0)
    flags2 = BitField(flags=("FLAG5", "FLAG6", "FLAG7", "FLAG8"), default=0)
    flags = BitField(("flags1", "flags2"))
