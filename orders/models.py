from django.db import models
from products.models import *
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order #{self.id} - Total: ${self.total_price:.2f}"

class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"CartItem #{self.id} - {self.product} - Quantity: {self.quantity} - Subtotal: ${self.subtotal:.2f}"

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
        order_items = self.order.cartitem_set.all()
        self.order.total_price = sum(item.subtotal for item in order_items)
        self.order.save()

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Order History #{self.id} - {self.ordered_date} - Total: ${self.total_price:.2f}"

class OrderHistoryItem(models.Model):
    order_history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def product_details(self):
        return f"{self.product.brand_name} - {self.product.description}"
