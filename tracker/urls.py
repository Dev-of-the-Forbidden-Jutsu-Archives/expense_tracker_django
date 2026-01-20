
from django.urls import path
from tracker.views import index, login_view, logout_view, register_view
from tracker.views import delete_transaction



urlpatterns = [
    path("", index, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('delete-transaction/<id>/', delete_transaction, name='delete-transaction'),
   
]
