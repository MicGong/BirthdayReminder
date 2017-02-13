from django.db import models

class Email(models.Model):
    # name = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=300)
    body = models.TextField()
    # create_date = models.DateField(auto_now=True)
