# -*- coding: utf-8 -*-
from django.urls import reverse, resolve
from credit_approval.views import (
    RegisterCustomerView,
    CheckEligibilityView,
    CreateLoanView,
    ViewLoanView,
    ViewLoansByCustomerView,
)


def test_register_url_resolves():
    url = reverse("register")
    assert resolve(url).func.view_class == RegisterCustomerView


def test_check_eligibility_url_resolves():
    url = reverse("check-eligibility")
    assert resolve(url).func.view_class == CheckEligibilityView


def test_create_loan_url_resolves():
    url = reverse("create-loan")
    assert resolve(url).func.view_class == CreateLoanView


def test_view_loan_url_resolves():
    url = reverse("view-loan", kwargs={"loan_id": 1})
    assert resolve(url).func.view_class == ViewLoanView


def test_view_loans_by_customer_url_resolves():
    url = reverse("view-loans", kwargs={"customer_id": 1})
    assert resolve(url).func.view_class == ViewLoansByCustomerView
