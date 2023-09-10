from django.db import models
from account.models import User
from django.shortcuts import get_object_or_404
from .validators import validate_icon_image_size, validate_image_file_extension,validate_banner_image_size


def server_banner_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"


def server_icon_path(instance, filename):
    return f"server/{instance.id}/server_icon/{filename}"


def category_icon_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.FileField(null=True, blank=True, upload_to=category_icon_path)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            obj = get_object_or_404(Category, id=self.id)
            if obj.icon != self.icon:
                obj.icon.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.icon.delete()
        super().delete(using=None, keep_parents=False)


class Server(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='server_owner')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='server_category')
    members = models.ManyToManyField(User, related_name='server_members', null=True, blank=True)

    banner = models.ImageField(null=True, blank=True, upload_to=server_banner_path, validators=[
        validate_banner_image_size,
        validate_image_file_extension,
    ]
                               )
    icon = models.ImageField(null=True, blank=True, upload_to=server_icon_path, validators=[
        validate_icon_image_size,
        validate_image_file_extension,
    ])

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        if self.id:
            obj = get_object_or_404(Server, id=self.id)
            if obj.icon != self.icon:
                obj.icon.delete(save=False)
            if obj.banner != self.banner:
                obj.banner.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.icon.delete()
        self.banner.delete()
        super().delete(using=None, keep_parents=False)

    def __str__(self):
        return self.title


class Channels(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel_owner')
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channel_server')

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title) + ' | ' + str(self.owner.username)
