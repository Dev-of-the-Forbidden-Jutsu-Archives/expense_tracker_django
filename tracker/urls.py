
from django.urls import path
from tracker.views import index
from tracker.views import delete_transaction



urlpatterns = [
    path("", index, name="home"),
    path('delete-transaction/<id>/', delete_transaction, name='delete-transaction'),
   
]
