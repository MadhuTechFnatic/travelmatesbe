from django.db import models

class TripSample(models.Model):
    title = models.CharField(max_length = 200)
    image_url = models.URLField()
    content = models.TextField()
    category = models.CharField(max_length=200)
    
