import datetime
from django.db.models import Sum


def calculate_emi(principal, annual_interest_rate, tenure_months):
    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero")
    r = annual_interest_rate / (12 * 100)
    n = tenure_months
    if r == 0:
        return principal / n
    emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return round(emi, 2)


def round_to_nearest_lakh(amount):
    return int(round(amount / 100000.0)) * 100000


def calculate_credit_score(customer, loan_queryset, now=None):
    # now is for testing; defaults to today
    now = now or datetime.date.today()
    loans = loan_queryset.filter(customer=customer)
    score = 100

    # 1 Past Loans paid on time
    paid_loans = loans.filter(end_date__lt=now)
    if paid_loans.exists():
        total_emis_paid_on_time = paid_loans.aggregate(Sum("emis_paid_on_time"))["emis_paid_on_time__sum"] or 0
        total_tenure = paid_loans.aggregate(Sum("tenure"))["tenure__sum"] or 0
        on_time_ratio = total_emis_paid_on_time / max(1, total_tenure)
        score -= int((1 - on_time_ratio) * 40)  # Up to -40 for missed payments

    # 2 No of loans taken in past
    num_loans = loans.count()
    if num_loans > 5:
        score -= min((num_loans - 5) * 2, 10)  # up to -10

    # 3 Loan activity in current year
    current_year = now.year
    this_year_loans = loans.filter(start_date__year=current_year)
    score -= min(this_year_loans.count() * 2, 10)  # up to -10

    # 4 Loan approved volume
    volume = loans.aggregate(Sum("loan_amount"))["loan_amount__sum"] or 0
    if volume > customer.approved_limit:
        score -= 20

    # 5 If sum of current loans > approved limit => score = 0
    active_loans = loans.filter(end_date__gte=now)
    active_loans_sum = active_loans.aggregate(Sum("loan_amount"))["loan_amount__sum"] or 0
    if active_loans_sum > customer.approved_limit:
        score = 0

    return max(0, min(100, score))


def determine_interest_rate(credit_rating, requested_interest):
    """
    Returns (approval, corrected_interest_rate)
    """
    if credit_rating > 50:
        return True, requested_interest
    elif 50 >= credit_rating > 30:
        return True, max(requested_interest, 12.0)
    elif 30 >= credit_rating > 10:
        return True, max(requested_interest, 16.0)
    else:
        return False, max(requested_interest, 16.0)
