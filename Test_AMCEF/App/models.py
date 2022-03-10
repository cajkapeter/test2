from django.db import models


class Post(models.Model):
    id = models.IntegerField(primary_key=True) #auto increment??
    userId = models.IntegerField()
    title = models.CharField(max_length=50)
    body = models.TextField()