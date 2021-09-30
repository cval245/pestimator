from django.db import models
from django.conf import settings
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    company_name = models.TextField(null=True)
    address = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zip_code = models.IntegerField(null=True)
    estimates_remaining = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if (self.pk is None):
            # if being created and not updated
            self.estimates_remaining = 1
            # set first estimate as free
            super(UserProfile, self).save(*args, **kwargs)
        else:
            super(UserProfile, self).save(*args, **kwargs)


class PurchaseOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    session_id = models.CharField(max_length=200, blank=True)
    paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=19, decimal_places=4, blank=True)


class LineItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    quantity_purchased = models.IntegerField()
    product_id = models.CharField(max_length=200)
    line_item_id = models.CharField(max_length=200)


class ProductPrice(models.Model):
    price_id = models.CharField(max_length=200)
    price_description = models.CharField(max_length=200)
