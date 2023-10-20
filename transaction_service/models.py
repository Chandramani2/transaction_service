from django.db import models

class Transaction(models.Model):
    amount = models.FloatField(null=True)
    type = models.CharField(max_length=255)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)