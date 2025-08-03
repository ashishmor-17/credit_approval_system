# -*- coding: utf-8 -*-
import pytest
from model_bakery import baker
from credit_approval.models import Customer, Loan
from credit_approval.serializers import (
    CustomerSerializer,
    LoanDetailSerializer,
    ViewLoanSerializer,
    ViewLoansCustomerSerializer,
    RegisterCustomerResponseSerializer,
    CheckEligibilityResponseSerializer,
    CreateLoanResponseSerializer,
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


@pytest.mark.django_db
def test_view_loans_customer_serializer():
    loan = baker.make(Loan)
    serializer_data = {
        "loan_id": loan.id,
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_repayment,
        "repayments_left": loan.tenure - loan.emis_paid_on_time,
    }
    serializer = ViewLoansCustomerSerializer(data=serializer_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["loan_id"] == loan.id


def test_register_customer_response_serializer():
    resp_data = {
        "customer_id": 1,
        "name": "John Doe",
        "age": 30,
        "monthly_income": 5000,
        "approved_limit": 20000,
        "phone_number": "1234567890",
    }
    serializer = RegisterCustomerResponseSerializer(data=resp_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["name"] == "John Doe"


def test_check_eligibility_response_serializer():
    resp_data = {
        "customer_id": 1,
        "approval": True,
        "interest_rate": 9.0,
        "corrected_interest_rate": 9.0,
        "tenure": 24,
        "monthly_installment": 5000.0,
    }
    serializer = CheckEligibilityResponseSerializer(data=resp_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["approval"] is True


def test_create_loan_response_serializer():
    resp_data = {
        "loan_id": 5,
        "customer_id": 2,
        "loan_approved": True,
        "message": "Loan approved",
        "monthly_installment": 2100.0,
    }
    serializer = CreateLoanResponseSerializer(data=resp_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["loan_approved"] is True
