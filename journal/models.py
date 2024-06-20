# journal/models.py

from django.db import models
from django.utils import timezone

class Topic(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title

class Entry(models.Model):
    topic = models.ForeignKey(Topic, related_name='entries', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    emotion = models.CharField(max_length=50)  
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title
