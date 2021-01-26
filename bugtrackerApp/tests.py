from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .models import Bug, Project, Status

# Create your tests here.
verbose = False

def createUser(username, password):
    return User.objects.create(username=username, email="example@example.com", password=password)

def createProject(title, lead=None, description="default description", contributors=[]):
    project = Project.objects.create(title=title, project_lead=lead, description=description)
    project.project_contributors.set(contributors)
    return project

def createBug(title, creator, status, lead=None, contributors=[], description="default bug description", project=None):
    bug = Bug.objects.create(title=title, creator=creator, status=status, lead=lead, description=description, project=project)    
    bug.contributors.set(contributors)
    return bug
    
def createStatus(code, name="new status type", description="default status description"):
    return Status.objects.create(code=code, name=name, description=description)





class BugTests(TestCase):
    @classmethod
    def setUpClass(self):
        super(BugTests, self).setUpClass()
        pass

    def setUp(self):
        pass

    def test_bug_status_must_be_0_if_not_assigned(self):
        pass

class ViewTests(TestCase):
    @classmethod
    def setUpClass(self):
        super(ViewTests, self).setUpClass()
        self.Alice=createUser("Alice", "testuserpassword123")
        self.Bob=createUser("Bob", "testuserpassword123")
        self.Charlie=createUser("Charlie", "testuserpassword123")
        self.project=createProject("classified_project", lead=self.Bob, contributors=[self.Charlie])
        self.unassigned = createStatus(0, name="Unassigned", description="This bug has not been assigned to a developer yet")
        self.assigned = createStatus(1, name="Assigned", description="This bug has had a developer designated as lead")
        self.bug1=createBug(title="This is bug 1", creator=self.Charlie, status=self.unassigned, lead=self.Charlie, contributors=[self.Charlie], project=self.project)
        self.bug2=createBug(title="This is bug 2", creator=self.Charlie, status=self.unassigned, lead=self.Charlie, contributors=[self.Charlie], project=self.project)
        self.bug3=createBug(title="This is bug 3", creator=self.Bob, status=self.unassigned, lead=self.Bob, contributors=[self.Charlie, self.Bob])


    def setUp(self):
        client = Client()
        

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

    def test_project_view_displays_bugs_iff_associated_with_project(self):
        self.user=self.Bob
        self.client.force_login(self.user)

        bugs = Bug.objects.all()
        project_database_bugs = bugs.filter(project=self.project.id)
        response=self.client.get(reverse('project-detail', args=[self.project.id]))
        project_view_bugs = response.context["object_list"]

        for pbug in project_view_bugs:
            assert pbug in project_database_bugs
        for bug in  project_database_bugs:
            assert bug in project_view_bugs

        if verbose:
            print("All bugs in test database")
            for bug in bugs:
                print(bug)

            print("Bugs in response")
            for object in response.context["object_list"]:
                print(object)