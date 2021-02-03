from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timezone, timedelta

from .models import Bug, Project, Status

# Create your tests here.
verbose = False
TZ = timezone(timedelta(hours=8))

def createUser(username, password):
    return User.objects.create(username=username, email="example@example.com", password=password)

def createProject(title, lead=None, description="default description", contributors=[]):
    project = Project.objects.create(title=title, project_lead=lead, description=description)
    project.project_contributors.set(contributors)
    return project

def createBug(title, creator, status, lead=None, contributors=[], description="default bug description", project=None, **kwargs):
    date = datetime.now(TZ)
    if 'date' in kwargs.keys():
        date = kwargs['date']
    bug = Bug.objects.create(title=title, creator=creator, created_at=date, status=status, lead=lead, description=description, project=project)    
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

    # self.user=self.Bob
    #     self.client.force_login(self.user)

    #     project = { 'title':'test_project', 'description':'A default lead test project'}
    #     self.client.post(reverse('project-create'), 
    #             data={'title':project['title'], 'description':project['description']})
    #     assert Project.objects.get(title="test_project").project_lead == self.user

    # Currently this just throws errors after something has been created in the database. This does
    # not enforce behavior preventing creation of an item in the first place. What the tests need
    # to test is whether a command to create an invalid entry raises an error of some form. To
    # do this with the database requires adding validation to fields in the model (I believe)
    # Other things that should throw errors are changing the date and the last_modified date to be
    # anything other than the current time (at time of assignment). It should also not be possible to 
    # assign a non-existent status (actually, that should be enforced by model behavior. ...then again
    # part of the point of tests is also future proofing against, say, changing the model without 
    # considering how that will affect behavior). 
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


    def test_using_nonexistent_status_raises_exception(self):
        with self.assertRaises(ValueError):
            createBug(title="title", creator=self.Alice, lead=self.Bob, status=102343)
            createBug(title="title", creator=self.Alice, lead=self.Bob, status=91919)
        

    def test_bug_raises_error_without_a_creator(self):
        with self.assertRaises(TypeError):
            self.bug99=createBug(title="This is bug 99", status=self.unassigned)

    # Question about constraints posted to stack overflow
    # def test_created_at_is_exactly_date_created(self):
    #     current_date = datetime.now(TZ)
    #     past_date = datetime(year=current_date.year, month=current_date.month, day=current_date.day,
    #                             hour=current_date.hour, minute=current_date.minute,
    #                             second=current_date.second, microsecond=current_date.microsecond-11,
    #                             tzinfo=current_date.tzinfo)
    #     invalid_bug = {'title':"This is bug 3", 'creator':self.Bob, 'date':past_date, 'status':self.unassigned}
    #     with self.assertRaises(ValidationError):
    #         createBug(title=invalid_bug['title'], creator=invalid_bug['creator'], 
    #                     status=invalid_bug['status'], date=invalid_bug['date'])


    def test_last_modified_cannot_be_assigned_custom_time(self):
        pass

    def test_invalid_title_raises_exception(self):
        pass

    def invalid_creator_raises_exception(self):
        pass

    def invalid_lead_raises_exception(self):
        pass

    # How would duplicate contributor entries (eg: alice, bob, bob) affect the orm?
    def test_django_eliminates_duplicate_contributors(self):
        invalid_bug = {'title':'Duplicates in contributor column', 'creator':self.Alice, 
                        'status':self.assigned, 'lead':self.Alice, 
                        'contributors':[self.Bob, self.Charlie, self.Bob]}

        invalid_entry = createBug(title=invalid_bug['title'], creator=invalid_bug['creator'], 
                                    status=invalid_bug['status'], lead=invalid_bug['lead'], 
                                    contributors=invalid_bug['contributors'])
        if verbose:
            print(f"Title is: {invalid_entry.title}, creator is: {invalid_entry.creator}, \
                    status is: {invalid_entry.status}, lead is :{invalid_entry.lead}.")
            print(f"ContributorsManager: {invalid_entry.contributors.all()}")


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

    