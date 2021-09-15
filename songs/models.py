from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length = 150)
    artist = models.CharField(max_length = 150)
    album = models.CharField(max_length = 150)
    queue_position = models.IntegerField()

    class Meta:
        ordering = ['-queue_position']
    
    def __str__(self):
        return f'{self.title} {self.artist} {self.album} {self.queue_position}'
    
