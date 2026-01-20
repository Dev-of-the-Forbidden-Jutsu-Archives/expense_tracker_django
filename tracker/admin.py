from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Admin Portal"
admin.site.register(CurrentBalance)


@admin.action(description="Mark selected stories as Credit")
def make_credit(modeladmin, request, queryset):
    queryset.update(expense_type="CREDIT")


@admin.action(description="Mark selected stories as Debit")
def make_debit(modeladmin, request, queryset):
    for q in queryset:
            obj = TrackingHistroy.objects.get(id=q.id)
            if obj.amount > 0:
                  obj.amount = obj.amount*-1
                  obj.save()
    queryset.update(expense_type="DEBIT")

class TrackingHistoryAdmmin(admin.ModelAdmin):
     list_display = [
          "amount",
          "current_balance",
        "expense_type",
            "created_at",
            "desctiption",
            "display_age"
     ]
     actions = [make_credit, make_debit]
     def display_age(self, obj):
            if obj.amount < 0:
                    return "negative"
            else:   
                return "positive"
     
     search_fields = ["expense_type", "desctiption"]
     list_filter = ["expense_type"]
     ordering = ["-expense_type"]
admin.site.register(TrackingHistroy, TrackingHistoryAdmmin)
