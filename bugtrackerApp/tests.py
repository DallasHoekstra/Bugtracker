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
        self.Alice=createUser("Alice", "testuserpassword123")
        self.Bob=createUser("Bob", "testuserpassword123")
        self.Charlie=createUser("Charlie", "testuserpassword123")
        self.project=createProject("classified_project", lead=self.Bob, contributors=[self.Charlie])
        self.unassigned = createStatus(0, name="Unassigned", description="This bug has not been assigned to a developer yet")
        self.assigned = createStatus(1, name="Assigned", description="This bug has had a developer designated as lead")
        self.bug1=createBug(title="This is bug 1", creator=self.Charlie, status=self.assigned, lead=self.Charlie, contributors=[self.Charlie], project=self.project)
        self.bug2=createBug(title="This is bug 2", creator=self.Charlie, status=self.assigned, lead=self.Charlie, contributors=[self.Charlie], project=self.project)
        self.bug3=createBug(title="This is bug 3", creator=self.Bob, status=self.assigned, lead=self.Bob, contributors=[self.Charlie, self.Bob])
        self.bug4=createBug(title="This is bug 4", creator=self.Bob, status=self.unassigned)

    def setUp(self):
        pass

    def test_bug_status_must_be_0_iff_not_assigned(self):
        bugs_without_lead = Bug.objects.filter(lead_id=None)
        for bug in bugs_without_lead:
            if verbose:
                print(bug.status.code)
            assert bug.status.code == 0
        
        unassigned_bugs = Bug.objects.filter(status=1)
        for bug in unassigned_bugs:
            if verbose:
                print(bug.status.code)
            if bug.status.code == 0:
                if verbose:
                    print(bug.lead_id)
                    print(bug)
                assert bug.lead_id == None

    def test_bug_raises_error_without_a_creator(self):
        with self.assertRaises(TypeError):
            self.bug99=createBug(title="This is bug 99", status=self.unassigned)


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
        self.bug1=createBug(title="This is bug 1", creator=self.Charlie, status=self.assigned, lead=self.Charlie, contributors=[self.Charlie], project=self.project)
        self.bug2=createBug(title="This is bug 2", creator=self.Charlie, status=self.assigned, lead=self.Charlie, contributors=[self.Charlie], project=self.project)
        self.bug3=createBug(title="This is bug 3", creator=self.Bob, status=self.assigned, lead=self.Bob, contributors=[self.Charlie, self.Bob])

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

    def test_project_update_view_not_accessible_by_unauthorized_user(self):
        self.user=self.Alice
        self.client.force_login(self.user)

        response=self.client.get(reverse('project-update', args=[self.project.id]))
        self.assertEqual(response.status_code, 403)
    
    # Are the ones that check web-page/view functionality with database
    # more integration tests than a unit tests?
    def test_project_view_accessible_by_lead(self):
        self.user=self.Bob
        self.client.force_login(self.user)

        response=self.client.get(reverse('project-update', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_view_accessible_by_contributor(self):
        self.user=self.Charlie
        self.client.force_login(self.user)

        response=self.client.get(reverse('project-update', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_update_view_displays_at_least_expected_fields(self):
        self.user=self.Bob
        self.client.force_login(self.user)

        response=self.client.get(reverse('project-update', args=[self.project.id]))
        field_list = ["title", "lead", "contributors", "description"]

        if verbose:
            print(str(response.content))

        for field in field_list:
            assert field in str(response.content)

    def test_project_create_defaults_project_lead_to_user(self):
        self.user=self.Bob
        self.client.force_login(self.user)

        project = { 'title':'test_project', 'description':'A default lead test project'}
        self.client.post(reverse('project-create'), 
                data={'title':project['title'], 'description':project['description']})
        assert Project.objects.get(title="test_project").project_lead == self.user

    def test_project_create_uses_provided_project_lead(self):
        self.user=self.Bob
        self.client.force_login(self.user)

        project = { 'title':'test_project', 'description':'A default lead test project',
                    'project_lead':self.Alice.id }
        # form name is project_lead, model fieldname is project_lead_id
        self.client.post(reverse('project-create'), 
                data={'title':project['title'], 'description':project['description'],
                    'project_lead':project['project_lead']})
        project_lead_id = Project.objects.get(title="test_project").project_lead_id
        if verbose:
            print(f"project lead ID is {project_lead_id}, Alice ID is {self.Alice.id}")
        assert  project_lead_id == self.Alice.id





    # def test_project_update_view_updates_fields_as_expected(self):
    #     self.user=self.Bob
    #     self.client.force_login(self.user)

    #     response=self.client.get(reverse('project-update', args=[self.project.id]))

    