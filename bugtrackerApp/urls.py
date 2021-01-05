from django.urls import path
from . import views


urlpatterns = [
    # django trims the already-matched parts of a url when working with the include function. An empty string means that the url accessed
    # was /bugtrackerapp
    path('', views.home, name='bugtrackerapp-home'),
    path('about/', views.about, name='bugtrackerapp-about')
]


