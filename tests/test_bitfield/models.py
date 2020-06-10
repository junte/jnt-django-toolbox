# -*- coding: utf-8 -*-

from django.db import models

from jnt_django_toolbox.models.fields import BitField


class BitFieldTestModel(models.Model):
    flags = BitField(
        flags=("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"),
        default=3,
        db_column="another_name",
    )


class CompositeBitFieldTestModel(models.Model):
    flags_1 = BitField(
        flags=("FLAG_0", "FLAG_1", "FLAG_2", "FLAG_3"), default=0,
    )

    flags_2 = BitField(
        flags=("FLAG_4", "FLAG_5", "FLAG_6", "FLAG_7"), default=0,
    )
    flags = BitField(("flags_1", "flags_2"))
