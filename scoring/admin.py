from django.contrib import admin
from .models import Mortgage

@admin.register(Mortgage)
class MortgageAdmin(admin.ModelAdmin):
    list_display = (
        'borrower_name',
        'loan_amount',
        'property_value',
        'monthly_income',
        'monthly_payment',
        'shariah_type',
        'origination_date',
        'ltv',
        'dsr',
        'seasoning_months',
        'is_src_eligible',
    )
    list_filter = ('shariah_type',)
    search_fields = ('borrower_name',)
