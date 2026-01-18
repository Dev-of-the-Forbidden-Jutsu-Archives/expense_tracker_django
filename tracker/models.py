from django.db import models

# Create your models here.


class CurrentBalance(models.Model):
    current_balance = models.FloatField(default=0)

    def __str__(self):
        return f"Current Balance: {self.current_balance}"


class TrackingHistroy(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    amount = models.FloatField()
    expense_type = models.CharField(choices=(('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')), max_length=200)
    desctiption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.desctiption} - {self.amount} ({self.expense_type})"
    