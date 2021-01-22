from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .models import Bug, Project, Status

# Create your tests here.


def createUser(username, password):
    return User.objects.create(username=username, email="example@example.com", password=password)

def createProject(title, lead=None, description="default description", contributors=[]):
    project = Project.objects.create(title=title, project_lead=lead, description=description)
    project.project_contributors.set(contributors)
    return project

def createBug(title, creator, status, lead=None, contributors=[], description="default bug description"):
    bug = Bug.objects.create(title=title, creator=creator, lead=lead, description=description)
    bug.status.set(status.id)
    bug.contributors.set(contributors)
    return 
    

def createStatus(code, name="new status type", description="default status description"):
    return Status.objects.create(code=code, name=name, description=description)


class ViewTests(TestCase):
    def setUp(self):
        client = Client()
        self.Alice=createUser("Alice", "testuserpassword123")
        self.Bob=createUser("Bob", "testuserpassword123")
        self.Charlie=createUser("Charlie", "testuserpassword123")
        self.project=createProject("classified_project", lead=self.Bob, contributors=[self.Charlie])
        # self.unassigned = createStatus(0, name="Unassigned", description="This bug has not been assigned to a developer yet")
        # self.bug1=createBug(title="This is bug 1", creator=self.Charlie, status=self.unassigned, lead=self.Charlie, contributors=[self.Charlie])
        # self.bug2=createBug(title="This is bug 2", creator=self.Charlie, lead=self.Charlie, contributors=[self.Charlie])
        # self.bug3=createBug(title="This is bug 3", creator=self.Bob, lead=self.Bob, contributors=[self.Charlie, self.Bob])

    def test_project_view_not_accessible_by_unrelated_user(self):
        self.user=self.Alice
        self.client.force_login(self.user)
        response=self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

    def test_project_view_accessible_by_lead(self):
        self.user=self.Bob
        self.client.force_login(self.user)
        response=self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_view_accessible_by_contributor(self):
        self.user=self.Charlie
        self.client.force_login(self.user)
        response=self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    # def test_project_view_displays_bugs_associated_with_project(self):
    #     self.user=self.Bob
    #     self.client.force_login(self.user)
    #     bugs = self.project.bug_set.all()
    #     response=self.client.get(reverse('project-detail', args=[self.project.id]))
    #     print(bugs)