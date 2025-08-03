# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Customer, Loan
from .serializers import (
    RegisterCustomerSerializer,
    RegisterCustomerResponseSerializer,
    CheckEligibilitySerializer,
    CheckEligibilityResponseSerializer,
    CreateLoanSerializer,
    CustomerSerializer,
    ViewLoanSerializer,
    ViewLoansCustomerSerializer,
)
from .utils import calculate_emi, round_to_nearest_lakh, calculate_credit_score, determine_interest_rate
from datetime import date


class RegisterCustomerView(APIView):
    """
    Handels customer registration
    """

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        approved_limit = round_to_nearest_lakh(36 * data["monthly_income"])
        customer = Customer.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            phone_number=data["phone_number"],
            monthly_salary=data["monthly_income"],
            approved_limit=approved_limit,
        )
        response_data = {
            "customer_id": customer.id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number,
        }
        resp_serializer = RegisterCustomerResponseSerializer(response_data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)


class CheckEligibilityView(APIView):
    """
    Checks customer eligibility for a loan
    """

    def post(self, request):
        serializer = CheckEligibilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer = get_object_or_404(Customer, id=data["customer_id"])
        loans = Loan.objects.filter(customer=customer)

        # If sum of all current EMIs > 50% of monthly salary, don't approve
        active_loans = loans.filter(end_date__gte=date.today())
        total_emi = sum([l.monthly_repayment for l in active_loans])
        if total_emi > 0.5 * customer.monthly_salary:
            approval = False
            corrected_interest = max(data["interest_rate"], 16.0)
        else:
            # Calculate credit score
            credit_score = calculate_credit_score(customer, Loan.objects)
            approval, corrected_interest = determine_interest_rate(credit_score, data["interest_rate"])
            # If interest rate doesn't match, fix
            if corrected_interest > data["interest_rate"]:
                approval = False

        monthly_installment = (
            calculate_emi(data["loan_amount"], corrected_interest, data["tenure"]) if approval else None
        )

        resp_data = {
            "customer_id": customer.id,
            "approval": approval,
            "interest_rate": data["interest_rate"],
            "corrected_interest_rate": corrected_interest,
            "tenure": data["tenure"],
            "monthly_installment": monthly_installment if monthly_installment else 0.0,
        }
        resp_serializer = CheckEligibilityResponseSerializer(resp_data)
        return Response(resp_serializer.data, status=status.HTTP_200_OK)


class CreateLoanView(APIView):
    """
    Creates a new loan for a customer
    """

    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer = get_object_or_404(Customer, id=data["customer_id"])

        # Run eligibility
        loans = Loan.objects.filter(customer=customer)
        active_loans = loans.filter(end_date__gte=date.today())
        total_emi = sum([l.monthly_repayment for l in active_loans])
        if total_emi > 0.5 * customer.monthly_salary:
            return Response(
                {
                    "loan_id": None,
                    "customer_id": customer.id,
                    "loan_approved": False,
                    "message": "Current EMI exceeds 50% of monthly salary",
                    "monthly_installment": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        credit_score = calculate_credit_score(customer, Loan.objects)
        approval, corrected_interest = determine_interest_rate(credit_score, data["interest_rate"])
        if not approval:
            return Response(
                {
                    "loan_id": None,
                    "customer_id": customer.id,
                    "loan_approved": False,
                    "message": "Loan not approved as per current credit score/interest policy",
                    "monthly_installment": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        monthly_installment = calculate_emi(data["loan_amount"], corrected_interest, data["tenure"])
        # Create loan
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data["loan_amount"],
            tenure=data["tenure"],
            interest_rate=corrected_interest,
            monthly_repayment=monthly_installment,
            emis_paid_on_time=0,
            start_date=date.today(),
            end_date=date.today().replace(year=date.today().year + int(data["tenure"] // 12)),
        )

        return Response(
            {
                "loan_id": loan.id,
                "customer_id": customer.id,
                "loan_approved": True,
                "message": "Loan approved",
                "monthly_installment": monthly_installment,
            },
            status=status.HTTP_201_CREATED,
        )


class ViewLoanView(APIView):
    """
    View details of a specific loan
    """

    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)
        resp_data = {
            "loan_id": loan.id,
            "customer": CustomerSerializer(loan.customer).data,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "tenure": loan.tenure,
        }
        serializer = ViewLoanSerializer(resp_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewLoansByCustomerView(APIView):
    """
    View all loans for a specific customer
    """

    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        today = date.today()
        results = []
        for loan in loans:
            end_date = loan.end_date
            months_left = (end_date.year - today.year) * 12 + (end_date.month - today.month)
            repayments_left = max(0, months_left)
            results.append(
                {
                    "loan_id": loan.id,
                    "loan_amount": loan.loan_amount,
                    "interest_rate": loan.interest_rate,
                    "monthly_installment": loan.monthly_repayment,
                    "repayments_left": repayments_left,
                }
            )
        serializer = ViewLoansCustomerSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
