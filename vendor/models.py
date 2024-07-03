from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.vendor.name} - {self.amount}'
