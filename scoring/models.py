from django.db import models


SHARIAH_TYPES = [
    ('Murabaha', 'Murabaha'),
    ('Ijarah', 'Ijarah'),
    ('Musharakah', 'Musharakah'),
]

class Mortgage(models.Model):
    borrower_name = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    property_value = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    shariah_type = models.CharField(max_length=20, choices=SHARIAH_TYPES)
    origination_date = models.DateField()

    def ltv(self):
        return round((self.loan_amount / self.property_value) * 100, 2)

    def dsr(self):
        return round((self.monthly_payment / self.monthly_income) * 100, 2)

    def seasoning_months(self):
        from datetime import date
        delta = date.today() - self.origination_date
        return delta.days // 30

    def is_src_eligible(self):
        return self.ltv() <= 85 and self.dsr() <= 45 and self.seasoning_months() >= 3
