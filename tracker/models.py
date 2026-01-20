from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CurrentBalance(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_balance = models.FloatField(default=0)

    def __str__(self):
        return f"Current Balance: {self.current_balance}"


class TrackingHistroy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(choices=(('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')), max_length=200)
    desctiption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"The amout is {self.amount} and the expense type is {self.expense_type}"
    



class RequestLogs(models.Model):
    request_info = models.TextField()
    request_type = models.CharField(max_length=100)
    request_method = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request Type: {self.request_type} at {self.created_at}"
    