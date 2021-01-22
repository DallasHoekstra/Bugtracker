from django.db import models
from django.db.models import Q


class BugtrackerQuerySet(models.QuerySet): 
    def project_bugs(self, projectID):
        return self.filter(project_id=projectID)

    def user_projects(self, user):
        return self.filter(project_lead__id=user.id)

class BugManager(models.Manager):
    def get_queryset(self):
        return BugtrackerQuerySet(self.model, using=self._db)

    def get_project_bugs(self, projectID):
        return self.get_queryset().project_bugs(projectID)

class ProjectManager(models.Manager):
    def get_queryset(self):
        return BugtrackerQuerySet(self.model, using=self._db)

    def get_user_projects(self, user):
        return self.get_queryset().user_projects(user)