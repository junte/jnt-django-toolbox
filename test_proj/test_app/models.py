from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from jnt_django_toolbox.db.fields import GenericForeignKey


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PostCategory(models.Model):
    title = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="author"
    )

    def __str__(self):
        return str(self.user)


class Post(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="posts"
    )
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=512)
    description = models.TextField()
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blogs"
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    owner = GenericForeignKey()
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.content
