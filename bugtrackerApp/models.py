from django.db import models
from django.db.models.fields import related
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .managers import ProjectManager







# Models flow from top to bottom. A model referenced by a class must appear before it.
class Status(models.Model):
    code = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50, default="Unassigned")
    description = models.TextField(default="This bug has not been assigned to a employee yet.")

    def __str__(self):
        return self.name

class Project(models.Model):
    # Unique fields
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField()

    # Foreign Key Fields
    project_lead = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=True, null=True, related_name="project_lead")
    project_contributors = models.ManyToManyField(User, default=None, blank=True, null=True, related_name="project_contributors")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

class Bug(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    lead = models.ForeignKey(User, default=None, blank=True, null=True, on_delete=models.SET_NULL, related_name="lead")
    contributors = models.ManyToManyField(User, default=None, blank=True, null=True, related_name="contributors")
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=0)
    description = models.TextField()

    objects = ProjectManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bug-detail', kwargs={'pk': self.pk})

    
