# inventory/models.py
from item.models import Item
from django.db import models

class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    initial_stock_level = models.PositiveIntegerField(default=0)
    current_stock_level = models.PositiveIntegerField(default=0)

    def update_stock_level(self, sales_quantity=0, returns_quantity=0, restocks_quantity=0):
        """
        Update the current stock level based on sales, returns, and restocks.
        """
        # Adjust stock level
        self.current_stock_level = (
            self.current_stock_level - sales_quantity + returns_quantity + restocks_quantity
        )
        self.save()

    def __str__(self):
        return f"{self.item.name} - Current Stock: {self.current_stock_level}"

    def save(self, *args, **kwargs):
        # If this is the first time the object is saved, set current stock level to initial stock level
        if not self.pk:  # New instance, not yet saved
            self.current_stock_level = self.initial_stock_level
        super().save(*args, **kwargs)
