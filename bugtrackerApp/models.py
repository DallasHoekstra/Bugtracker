from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import related
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta

from .managers import ProjectManager, BugManager







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

    objects = ProjectManager()

class Iteration(models.Model):

    def iteration_end_date():
        now = timezone.now()
        return now + timedelta(days=7)

    title = models.CharField(max_length=50)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=iteration_end_date)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, default=None, blank=True, null=True, related_name="team_members")
    velocity = models.FloatField(default=.7)

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
    hours_to_finish = models.PositiveIntegerField(default=1)
    iteration = models.ForeignKey(Iteration, default=None, blank=True, null=True, on_delete=SET_NULL)

    objects = BugManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.project_id})




