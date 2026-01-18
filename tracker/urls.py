
from django.urls import path
from tracker.views import home



urlpatterns = [
    path("", home, name="home"),
   
]
