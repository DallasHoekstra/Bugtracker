from django.db.models.fields import PositiveIntegerField
from django.forms import forms
from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
import logging

from .models import Bug, Iteration, Project
from .managers import ProjectManager, BugtrackerQuerySet
from .forms import ProjectValidationMixin
# List, Detail, Create, Update, Delete views are available
# CRUD: Create, R(List, Detail), Update, Delete

logger = logging.getLogger(__name__)

def home(request):
    # values inside context will be available to the templates
    context = {
        'bugs': Bug.objects.all()
    }
    return render(request, 'bugtrackerApp/home.html', context)

class BugListView(ListView):
    context_object_name = 'bugs'
    model = Bug
    ordering = ['-created_at']


class UserBugListView(ListView):
    model = Bug
    template_name = 'bugtrackerApp/user_bugs.html' 
    context_object_name = 'bugs'
    #paginate_by = 1

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Bug.objects.filter(creator=user).order_by('-created_at')

class BugDetailView(DetailView):
    model = Bug

class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    fields = ['title', 'project', 'lead', 'contributors', 'status','description']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class BugUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bug
    fields = ['title', 'project', 'description', 'contributors', 'status', 'lead']

    def test_func(self):
        bug = self.get_object()
        if self.request.user == bug.creator:
            return True
        else:
            return False

class BugDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bug
    # home page
    success_url = '/'

    def test_func(self):
        bug = self.get_object()
        if self.request.user == bug.creator:
            return True
        else:
            return False

class ProjectCreateView(ProjectValidationMixin, LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'project_lead', 'project_contributors', 'description']
    success_url = ''

    # def form_valid(self, form):
    #     form.instance.project_lead = self.request.user
    #     return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'project_lead', 'project_contributors', 'description']

    def test_func(self):
        project = Project.objects.get(id=self.kwargs.get('pk'))
        contributors = project.project_contributors.all()
        lead = project.project_lead
        user = self.request.user
        if user == lead:
            return True
        if user in contributors:
            return True
        return False

class ProjectView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = "bugs"

    def get_queryset(self):
        project_bugs = Bug.objects.get_project_bugs(self.kwargs.get("pk"))
        return project_bugs
    
    def test_func(self):
        project = Project.objects.get(id=self.kwargs.get('pk'))
        contributors = project.project_contributors.all()
        lead = project.project_lead
        user = self.request.user
        if user == lead:
            return True
        if user in contributors:
            return True
        return False
            
class UserProjectsView(LoginRequiredMixin, ListView):
    context_object_name="projects"

    def get_queryset(self):
        user_projects = Project.objects.get_user_projects(self.request.user)
        return user_projects

class IterationCreateView(LoginRequiredMixin, CreateView):
    model = Iteration
    fields = ['title', 'start_date', 'end_date', 'project', 'team_members', 'velocity']

    def get_success_url(self):
        return reverse('burndown-chart', kwargs={'pk': self.object.pk})

    # def test_func(self):
    #     project = Project.objects.get(id=self.kwargs.get('pk'))
    #     #contributors = project.project_contributors.all()
    #     lead = project.project_lead
    #     user = self.request.user
    #     if user == lead:
    #         return True
    #     #if user in contributors:
    #      #   return True
    #     return False

class IterationView(LoginRequiredMixin, ListView):
    context_object_name="bugs"
    model=Iteration

    def post(self, request, *args, **kwargs):
        for bug in request.POST:
            logger.warning(bug)
        request_dict = request.POST
        # sanitize contents of dictionary here
        logger.warning(JsonResponse(request.POST, status=200))

        

        return JsonResponse(request.POST, status=200)


    def get_queryset(self):
        iteration = Iteration.objects.get(id=self.kwargs.get('pk'))
        project_id = iteration.project_id
        logger.warning(project_id)
        bugs = Bug.objects.get_project_bugs(project_id)
        return bugs
        # for bug in bugs:
        #     logger.warning(f'bug is {bug}')
        # if bugs:
        #     return bugs
           
    # def get_object(self):
    #      return Iteration.objects.get(id=self.kwargs.get('pk'))





    # def test_func(self):
    #     project = Project.objects.get(id=self.kwargs.get('pk'))
    #     contributors = project.project_contributors.all()
    #     lead = project.project_lead
    #     user = self.request.user
    #     if user == lead:
    #         return True
    #     if user in contributors:
    #         return True
    #     return False

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'bugtrackerApp/about.html', context)


