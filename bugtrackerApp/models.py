from django.db import models
from django.db.models.fields import related
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Models flow from top to bottom. A model referenced by a class must appear before it.
class Status(models.Model):
    code = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50, default="Unassigned")
    description = models.TextField(default="This bug has not been assigned to a employee yet.")

    def __str__(self):
        return self.name

class Bug(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    lead = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL, related_name="lead")
    contributors = models.ManyToManyField(User, default=None, blank=True, null=True, related_name="contributors")
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=0)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bug-detail', kwargs={'pk': self.pk})

