from django.db import models


# Create your models here.

class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title
