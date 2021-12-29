# flake8: noqa
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("test_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="comment",
            name="content_type",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="contenttypes.contenttype"),
        ),
        migrations.AddField(
            model_name="blog",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="blogs", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="blog",
            name="tags",
            field=models.ManyToManyField(blank=True, to="test_app.Tag"),
        ),
        migrations.AddField(
            model_name="author",
            name="user",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="author", to=settings.AUTH_USER_MODEL),
        ),
    ]
