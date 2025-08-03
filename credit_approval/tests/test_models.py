# -*- coding: utf-8 -*-
import pytest
from model_bakery import baker
from django.db import IntegrityError
from credit_approval.models import Customer, Loan


@pytest.mark.django_db
def test_create_customer():
    customer = baker.make(Customer)
    assert isinstance(customer.first_name, str)
    assert isinstance(customer.last_name, str)
    assert isinstance(customer.phone_number, str)
    assert isinstance(customer.monthly_salary, int)
    assert isinstance(customer.approved_limit, int)
    assert isinstance(customer.age, int)
    assert isinstance(customer.current_debt, int)
    assert customer.phone_number  # not blank
    assert str(customer) == f"{customer.first_name} {customer.last_name}"


@pytest.mark.django_db
def test_customer_unique_phone_number():
    customer1 = baker.make(Customer, phone_number="1112223333")
    with pytest.raises(IntegrityError):
        baker.make(Customer, phone_number=customer1.phone_number)


@pytest.mark.django_db
def test_customer_default_values():
    customer = baker.make(Customer)
    assert customer.age == 0
    assert customer.current_debt == 0


@pytest.mark.django_db
def test_create_loan():
    loan = baker.make(Loan)
    assert isinstance(loan.customer, Customer)
    assert isinstance(loan.loan_amount, float)
    assert isinstance(loan.tenure, int)
    assert isinstance(loan.interest_rate, float)
    assert isinstance(loan.monthly_repayment, float)
    assert isinstance(loan.emis_paid_on_time, int)
    assert loan.start_date is not None
    assert loan.end_date is not None
    assert str(loan) == f"Loan #{loan.id} for {loan.customer}"


@pytest.mark.django_db
def test_loan_str():
    loan = baker.make(Loan)
    loan_str = str(loan)
    assert f"Loan #{loan.id} for {loan.customer}" == loan_str
