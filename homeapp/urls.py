from django.contrib import admin
from django.urls import path
from homeapp import views  # ✅ Bas yeh hi import chahiye

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Main Pages
    path('', views.home, name='home'),
    path('contact/', views.contact_page, name='contact'),
    path('help/', views.help_page, name='help'),
    path('buy/', views.buy, name='buy'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order_view, name='place_order'),

    # ✅ Auth Views
    path('login/', views.login_signup_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ✅ Cart Views
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_quantity, name='update_quantity'),

    # ✅ User Section
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
    path('invoice/<str:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('cancel-order/<str:order_id>/', views.cancel_order, name='cancel_order'),
    path('profile/', views.user_profile, name='user_profile'),
]
