from django.db import models


class Customer(models.Model):  # customer model for the credit approval system
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.PositiveIntegerField()
    approved_limit = models.PositiveIntegerField()
    current_debt = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):  # loan model for the credit approval system
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.FloatField()
    tenure = models.PositiveIntegerField()  # in months
    interest_rate = models.FloatField()
    monthly_repayment = models.FloatField()
    emis_paid_on_time = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan #{self.id} for {self.customer}"
