from django.urls import path

from .views import BugListView, BugDetailView, BugCreateView, BugUpdateView, BugDeleteView
from . import views



urlpatterns = [
    # django trims the already-matched parts of a url when working with the include function. An empty string means that the url accessed
    # was /bugtrackerapp
    path('', BugListView.as_view(), name='bugtrackerapp-home'),
    path('about/', views.about, name='bugtrackerapp-about'),

    path('bug/<int:pk>/', BugDetailView.as_view(), name='bug-detail'),
    path('bug/<int:pk>/update/', BugUpdateView.as_view(), name='bug-update'),
    path('bug/<int:pk>/delete/', BugDeleteView.as_view(), name='bug-delete'),
    path('bug/new/', BugCreateView.as_view(), name='bug-create')
    
]


