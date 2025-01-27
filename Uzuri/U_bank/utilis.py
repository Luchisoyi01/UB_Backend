from django.db.models import Sum
from .models import Account

def calculate_total_accounts():
  # Aggregate totals for each field
  totals = Account.objects.aggregate(
    total_fixed=Sum('Fixed_Account'),
    total_salary=Sum('Salary_Account'),
    total_savings=Sum('Savings_Account')
  )
  # Calculate grand total
  grand_total = (totals['total_fixed'] or 0) + (totals['total_salary'] or 0) + (totals['total_savings'] or 0)

  return {
    'totals': totals,
    'grand_total': grand_total
  }


def calculate_grand_total():
  # Aggregate all monetary fields to calculate the grand total
  totals = Account.objects.aggregate(
    total_fixed=Sum('Fixed_Account'),
    total_salary=Sum('Salary_Account'),
    total_savings=Sum('Savings_Account')
  )
  # Calculate grand total
  grand_total = (totals['total_fixed'] or 0) + (totals['total_salary'] or 0) + (totals['total_savings'] or 0)
  return grand_total
  