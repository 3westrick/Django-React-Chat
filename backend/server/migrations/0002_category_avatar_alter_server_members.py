# Generated by Django 4.2.5 on 2023-09-09 16:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("server", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="avatar",
            field=models.ImageField(default="avatar.svg", null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="server",
            name="members",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="server_members",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
