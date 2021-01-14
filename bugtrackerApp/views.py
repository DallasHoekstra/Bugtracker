from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Bug


# List, Detail, Create, Update, Delete views are available
# CRUD: Create, R(List, Detail), Update, Delete

def home(request):
    # values inside context will be available to the templates
    context = {
        'bugs': Bug.objects.all()
    }
    return render(request, 'bugtrackerApp/home.html', context)

class BugListView(ListView):
    model = Bug
    template_name = 'bugtrackerApp/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'bugs'
    ordering = ['-created_at']
    #paginate_by = 1

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
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class BugUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bug
    fields = ['title', 'description', 'status']

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

    



def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'bugtrackerApp/about.html', context)


