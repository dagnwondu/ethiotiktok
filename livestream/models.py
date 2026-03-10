from django.db import models
from django.conf import settings
# Create your models here.
class Video(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_uploaders' )
    video_file = models.FileField(upload_to="videos/")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_videos")
    created_at = models.DateTimeField(auto_now_add=True)

class LiveStream(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    guests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="guest_streams", blank=True)
    title = models.CharField(max_length=255)
    is_live = models.BooleanField(default=False)
    viewers_count = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)