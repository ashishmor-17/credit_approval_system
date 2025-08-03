# -*- coding: utf-8 -*-
import pytest
from model_bakery import baker
from credit_approval.models import Customer, Loan
from credit_approval.serializers import (
    CustomerSerializer,
    LoanDetailSerializer,
    ViewLoanSerializer,
    ViewLoansCustomerSerializer,
)


@pytest.mark.django_db
def test_customer_serializer():
    customer = baker.make(Customer)
    data = CustomerSerializer(customer).data
    assert data["id"] == customer.id
    assert data["first_name"] == customer.first_name
    assert data["last_name"] == customer.last_name
    assert data["phone_number"] == customer.phone_number


@pytest.mark.django_db
def test_loan_detail_serializer():
    loan = baker.make(Loan)
    data = LoanDetailSerializer(loan).data
    assert data["id"] == loan.id
    assert data["customer"]["id"] == loan.customer.id
    assert data["loan_amount"] == loan.loan_amount
    assert data["interest_rate"] == loan.interest_rate
    assert data["monthly_repayment"] == loan.monthly_repayment
    assert data["tenure"] == loan.tenure


@pytest.mark.django_db
def test_view_loan_serializer():
    loan = baker.make(Loan)
    # Use instance for output serializer
    serializer = ViewLoanSerializer(
        instance={
            "loan_id": loan.id,
            "customer": loan.customer,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "tenure": loan.tenure,
        }
    )
    data = serializer.data
    assert data["loan_id"] == loan.id
    assert data["customer"]["id"] == loan.customer.id
    assert data["loan_amount"] == loan.loan_amount
    assert data["interest_rate"] == loan.interest_rate
    assert data["monthly_installment"] == loan.monthly_repayment
    assert data["tenure"] == loan.tenure


@pytest.mark.django_db
def test_view_loans_customer_serializer():
    loan = baker.make(Loan)
    repayments_left = max(0, loan.tenure - loan.emis_paid_on_time)
    # Use instance for output serializer
    serializer = ViewLoansCustomerSerializer(
        instance={
            "loan_id": loan.id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "repayments_left": repayments_left,
        }
    )
    data = serializer.data
    assert data["loan_id"] == loan.id
    assert data["loan_amount"] == loan.loan_amount
    assert data["interest_rate"] == loan.interest_rate
    assert data["monthly_installment"] == loan.monthly_repayment
    assert data["repayments_left"] == repayments_left
