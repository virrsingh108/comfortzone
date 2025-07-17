from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

# ✅ Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# ✅ Order Model (now with phone field added)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)  # ✅ Added here
    email = models.EmailField()
    address = models.TextField()
    quantity = models.IntegerField(default=1)
    order_id = models.CharField(max_length=100, unique=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = "CZ" + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.customer_name} - {self.product.name}"

# ✅ Login Log Model
class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    login_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
