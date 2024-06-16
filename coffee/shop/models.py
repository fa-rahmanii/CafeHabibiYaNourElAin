from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Storage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} - {self.amount}g"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def max_purchase_quantity(self):
        quantities = [
            pi.storage.amount // pi.amount
            for pi in self.productingredient_set.all()
        ]
        return min(quantities) if quantities else 0
    
    def can_be_purchased(self, quantity):
        product_ingredients = self.productingredient_set.all()
        for pi in product_ingredients:
            if pi.amount * quantity > pi.storage.amount:
                return False
        return True

class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Cart'),
        ('completed', 'Completed'),
    ]
    
    DELIVERY_CHOICES = [
        ('outside', 'Outside'),
        ('in_person', 'In Person'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_amount = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='in_person')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.product}"

class SliderItem(models.Model):
    image = models.ImageField(upload_to='slider_images/')

    def __str__(self):
        return f"Image {self.id}"
    
class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.storage.name} - {self.amount}"
    
class PurchaseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PurchaseRecord {self.id} by {self.user.username}'
