from django.db import models
from autoslug import AutoSlugField
from django.utils.html import format_html
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, null=False, blank=True)
    description = models.TextField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to="category_images", null=False, blank=False)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    creator = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return format_html("<img src='/media/{}' style='width:70px;'>".format(self.image))

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=True)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to="post_images", null=False, blank=False)
    video = models.FileField(upload_to="post_videos", null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    creator = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProfileName(models.Model):
    profile_name = models.CharField(max_length=100, null=False, blank=True)
    username = models.CharField(max_length=100, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile_name
