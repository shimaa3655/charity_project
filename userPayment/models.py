from django.db import models

# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    item_name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=3)
    invoice = models.CharField(max_length=50)
    custom = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment {self.pk}"
