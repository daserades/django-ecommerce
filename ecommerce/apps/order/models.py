from django.db import models

from apps.product.models import Product

from apps.vendor.models import Vendor
from apps.customer.models import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer,  related_name='orders',on_delete=models.CASCADE,)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount= models.DecimalField(max_digits=8, decimal_places=2)
    vendors= models.ManyToManyField(Vendor, related_name='orders')

    class Meta:
        ordering= ['-created_at']

    def __str__(self):
        return self.customer.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE)
    vendor_paid=models.BooleanField(default=False)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    quantity= models.IntegerField(default=1)
    
    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price*self.quantity