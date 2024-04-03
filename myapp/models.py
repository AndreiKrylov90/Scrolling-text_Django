from django.db import models


class RequestData(models.Model):
    text = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
