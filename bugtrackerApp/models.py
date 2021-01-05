from django.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.utils import timezone
from django.contrib.auth.models import User

class Bug(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return self.title