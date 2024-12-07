from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name_category


class Ads(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='ads_images', blank=True, null=True)
    video = models.FileField(upload_to='ads_videos', blank=True, null=True)
    time_create = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.title


class Reply(models.Model):
    post = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username + ', ' + self.post.title
