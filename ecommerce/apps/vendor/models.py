from django.db import models
from apps.customer.models import User

class Vendor(models.Model):
    created_by = models.OneToOneField(User,related_name='vendor',on_delete=models.CASCADE, primary_key=True)
    name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['name']

    
    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.created_by.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.created_by.id])
        return sum((item.product.price * item.quantity) for item in items)