from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Recording(models.Model):
    filename = models.TextField(blank=True)
    prompt = models.CharField(max_length=200)
    user = models.CharField(max_length=50)
    voice_record = models.FileField(upload_to='speechtotask/audio/')
    date_posted = models.DateTimeField(auto_now_add=True)
    transcription = models.FileField(upload_to='speechtotask/transcriptions/', null=True)
    transcription_url = models.FileField(upload_to='speechtotask/metadata/', null=True)
    chunkId= models.PositiveIntegerField(default = 0)
    startId = models.PositiveIntegerField(default=0)
    processed = models.BooleanField(default=False)

class Summary(models.Model):
    recordingId = models.ForeignKey(Recording, on_delete=models.CASCADE)
    chunkId = models.PositiveIntegerField(default=0)
    startId = models.PositiveIntegerField(default=0)
    summaryChunk = models.TextField(blank=True)
