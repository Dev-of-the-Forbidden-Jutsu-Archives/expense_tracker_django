from math import e
from django.shortcuts import redirect, render

from tracker.models import CurrentBalance, TrackingHistroy
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method == "POST":
        description = request.POST.get("description")
        amount = request.POST.get("amount")

        current_balance,_ = CurrentBalance.objects.get_or_create(id=1)

        expense_type = "CREDIT"

        if float(amount) <0:
          
            expense_type="DEBIT"
        if float(amount) == 0:
            messages.error(request, "Amount cannot be zero.")
            return redirect("home")

        tracking_histroy = TrackingHistroy.objects.create(
            amount=amount,
            expense_type=expense_type,
            desctiption=description,
            current_balance=current_balance,
        )
        current_balance.current_balance += float(tracking_histroy.amount)   
        current_balance.save()


        return redirect("home")
    current_balance,_ = CurrentBalance.objects.get_or_create(id=1)
    income = 0
    expense = 0

    for tracking_histroy in TrackingHistroy.objects.all():
        if tracking_histroy.expense_type == "CREDIT":
            income += tracking_histroy.amount
        else:
            expense += tracking_histroy.amount


    context = {'income':income,'expense':expense,'transtions':TrackingHistroy.objects.all(), 'current_balance': current_balance}
    return render(request, "index.html", context)




def delete_transaction(request, id):
    traction_histroy = TrackingHistroy.objects.filter(id=id)
    if traction_histroy.exists():
        current_balance,_ = CurrentBalance.objects.get_or_create(id=1)
        tracking_histroy = traction_histroy[0]
       
        current_balance.current_balance = current_balance.current_balance - tracking_histroy.amount

        current_balance.save()
    traction_histroy.delete()
    return redirect("home")