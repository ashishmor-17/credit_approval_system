# -*- coding: utf-8 -*-
from celery import shared_task
import pandas as pd
from .models import Customer, Loan


@shared_task
def ingest_customer_data():
    df = pd.read_excel("data/customer_data.xlsx")
    print(df.columns)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            id=row["Customer ID"],
            defaults={
                "first_name": row["First Name"],
                "last_name": row["Last Name"],
                "age": row["Age"],
                "phone_number": str(row["Phone Number"]),
                "monthly_salary": row["Monthly Salary"],
                "approved_limit": row["Approved Limit"],
            },
        )


@shared_task
def ingest_loan_data():
    df = pd.read_excel("data/loan_data.xlsx")
    print(df.columns)
    for _, row in df.iterrows():
        customer = Customer.objects.get(id=row["Customer ID"])
        Loan.objects.update_or_create(
            id=row["Loan ID"],
            defaults={
                "customer": customer,
                "loan_amount": row["Loan Amount"],
                "tenure": row["Tenure"],
                "interest_rate": row["Interest Rate"],
                "monthly_repayment": row["Monthly payment"],
                "emis_paid_on_time": row["EMIs paid on Time"],
                "start_date": row["Date of Approval"],
                "end_date": row["End Date"],
            },
        )
