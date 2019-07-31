from django.db import models
from billing.models import BillingProfile

ADDRESSES_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Addresses(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESSES_TYPES)
    address_line1 = models.CharField(max_length=120)
    address_line2 = models.CharField(max_length=120, null=True, blank=True)
    province = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1}\n{line2}\n{postal}\n{city}, \n{province}, \n{country}".format(line1=self.address_line1,
                                                                          line2=self.address_line2 or '',
                                                                          postal = self.postal_code,
                                                                          city = self.city,
                                                                          province = self.province,
                                                                          country = self.country)