from django.db import models


class Order(models.Model):
    customer = models.ForeignKey("customers.Customer", on_delete=models.CASCADE)
    amount_cents = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=64)

    class Meta:
        db_table = "orders"
