from django.contrib import admin
from .models import Product, Order, LoginLog
from django.contrib.admin import AdminSite

# ✅ Brand the Admin Panel
admin.site.site_header = "ComfortZone Admin Panel 🛋️"
admin.site.site_title = "ComfortZone Admin"
admin.site.index_title = "Welcome to ComfortZone Dashboard"

# ✅ Product Admin View
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    list_filter = ['price']
    ordering = ['-id']

# ✅ Order Admin View (🔧 Added phone number field)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'phone', 'product', 'quantity', 'ordered_at']
    list_display_links = ['order_id', 'customer_name']
    list_filter = ['ordered_at']
    search_fields = ['order_id', 'customer_name', 'email', 'phone']
    readonly_fields = ['order_id', 'ordered_at']
    ordering = ['-ordered_at']

# ✅ Login Log Admin View
@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'login_time']
    search_fields = ['user__username']
    list_filter = ['login_time']
    ordering = ['-login_time']
