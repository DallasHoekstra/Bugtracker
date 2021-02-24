from .models import Project

class ProjectValidationMixin():
    def form_valid(self, form):
        if form.instance.project_lead == None:
            form.instance.project_lead = self.request.user
        return super().form_valid(form)

class BugValidationMixin():
    pass