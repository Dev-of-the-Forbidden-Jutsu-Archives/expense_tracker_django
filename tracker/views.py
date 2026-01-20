from math import e
import re
from django.shortcuts import redirect, render

from tracker.models import CurrentBalance, TrackingHistroy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, "User does not exist.")
            return redirect("/login/")
    
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("/login/")
    return render(request, "login.html")

def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")


        user = User.objects.filter(username=username)
        if user.exists():
            messages.success(request, "Username is already taken.")
            return redirect("/register/")
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        CurrentBalance.objects.create(
            user=user
        )
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")
    return render(request, "register.html")



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        description = request.POST.get("description")
        amount = request.POST.get("amount")

        current_balance,_ = CurrentBalance.objects.get_or_create(
            user = request.user
        )

        expense_type = "CREDIT"

        if float(amount) <0:
          
            expense_type="DEBIT"
        if float(amount) == 0:
            messages.error(request, "Amount cannot be zero.")
            return redirect("home")

        tracking_histroy = TrackingHistroy.objects.create(
            user = request.user,
            amount=amount,
            expense_type=expense_type,
            desctiption=description,
            current_balance=current_balance,
        )
        current_balance.current_balance += float(tracking_histroy.amount)   
        current_balance.save()


        return redirect("home")
    current_balance,_ = CurrentBalance.objects.get_or_create(user=request.user)
    income = 0
    expense = 0

    for tracking_histroy in TrackingHistroy.objects.filter(user=request.user):
        if tracking_histroy.expense_type == "CREDIT":
            income += tracking_histroy.amount
        else:
            expense += tracking_histroy.amount


    context = {'income':income,'expense':expense,'transtions':TrackingHistroy.objects.filter(user=request.user), 'current_balance': current_balance}
    return render(request, "index.html", context)



@login_required(login_url="login")
def delete_transaction(request, id):
    tracking_histroy = TrackingHistroy.objects.filter(
        id=id,
        user=request.user
    ).first()
    if tracking_histroy:
       current_balance = tracking_histroy.current_balance
       current_balance.current_balance -= tracking_histroy.amount
       current_balance.save()
       tracking_histroy.delete()
    return redirect("home")

