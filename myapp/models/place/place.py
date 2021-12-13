from django.db import models

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    placeName = models.CharField(max_length=32)
    placeId = models.CharField(max_length=32)
    parent = models.CharField(max_length=32)