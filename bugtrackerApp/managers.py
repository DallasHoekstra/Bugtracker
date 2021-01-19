from django.db import models


class ProjectQuerySet(models.QuerySet): 
    def project_bugs(self, projectID):
        return self.filter(project_id=projectID)

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def get_project_bugs(self, projectID):
        return self.get_queryset().project_bugs(projectID)

