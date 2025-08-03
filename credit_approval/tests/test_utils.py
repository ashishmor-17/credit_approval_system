# -*- coding: utf-8 -*-
import pytest
from model_bakery import baker
import datetime
from credit_approval.models import Customer, Loan
from credit_approval.utils import calculate_emi, round_to_nearest_lakh, calculate_credit_score, determine_interest_rate


def test_calculate_emi_normal_case():
    emi = calculate_emi(120000, 12, 12)
    assert isinstance(emi, float)
    assert round(emi, 2) == emi


def test_calculate_emi_zero_interest():
    emi = calculate_emi(120000, 0, 12)
    assert emi == 10000.0


def test_calculate_emi_invalid_tenure():
    with pytest.raises(ValueError):
        calculate_emi(100000, 10, 0)


def test_round_to_nearest_lakh():
    assert round_to_nearest_lakh(130000) == 200000
    assert round_to_nearest_lakh(250000) == 300000


@pytest.mark.django_db
def test_calculate_credit_score_basic():
    customer = baker.make(Customer, approved_limit=300000)
    score = calculate_credit_score(customer, Loan.objects)
    assert 0 <= score <= 100


@pytest.mark.django_db
def test_calculate_credit_score_active_volume_exceeds_limit():
    customer = baker.make(Customer, approved_limit=100000)
    now = datetime.date.today()
    baker.make(
        Loan,
        customer=customer,
        loan_amount=150000,
        start_date=now.replace(year=now.year - 1),
        end_date=now.replace(year=now.year + 1),
    )
    score = calculate_credit_score(customer, Loan.objects, now=now)
    assert score == 0


@pytest.mark.django_db
def test_calculate_credit_score_past_loans_paid_on_time():
    customer = baker.make(Customer, approved_limit=500000)
    now = datetime.date.today()
    # loan tenure 12, all emis paid on time
    baker.make(
        Loan,
        customer=customer,
        start_date=now.replace(year=now.year - 2),
        end_date=now.replace(year=now.year - 1),
        emis_paid_on_time=12,
        tenure=12,
        loan_amount=10000,
    )
    score = calculate_credit_score(customer, Loan.objects, now=now)
    assert score == 100


def test_determine_interest_rate():
    assert determine_interest_rate(80, 10) == (True, 10)
    assert determine_interest_rate(40, 10) == (True, 12.0)
    assert determine_interest_rate(20, 10) == (True, 16.0)
    assert determine_interest_rate(5, 10) == (False, 16.0)
