from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import Product, LoginLog, Order

# ✅ Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# ✅ Add to Cart
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if not product_id:
            messages.error(request, "Invalid product.")
            return redirect("home")

        cart = request.session.get("cart", {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session["cart"] = cart

        messages.success(request, "Item added to cart.")
        return redirect("home")
    return redirect("home")

# ✅ View Cart Page
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': total
            })
            total_price += total
        except Product.DoesNotExist:
            continue

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })

# ✅ Update Quantity in Cart
def update_quantity(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        action = request.POST.get('action')

        if product_id in cart:
            if action == 'increase':
                cart[product_id] += 1
            elif action == 'decrease':
                cart[product_id] = max(1, cart[product_id] - 1)

        request.session['cart'] = cart
    return redirect('cart')

# ✅ Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('cart')

# ✅ Login + Signup Combined View
def login_signup_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                LoginLog.objects.create(user=user)
                messages.success(request, f"Welcome back, {username}!")
            else:
                messages.error(request, "Invalid username or password.")

        elif action == 'signup':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                LoginLog.objects.create(user=user)
                messages.success(request, "Account created successfully!")

    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# ✅ PDF Invoice Generator
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    template_path = 'invoice_template.html'
    context = {'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{order.order_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF invoice')
    return response

# ✅ Cancel Order@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if order.status == 'Placed':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order {order.order_id} cancelled successfully.")
    else:
        messages.error(request, "This order cannot be cancelled.")
    return redirect('my_orders')

# ✅ User Profile@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

# ✅ Logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

# ✅ Static Pages
def contact_page(request):
    return render(request, 'contact.html')

def help_page(request):
    return render(request, 'help.html')

def checkout_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': total
            })
            total_price += total
        except Product.DoesNotExist:
            continue

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# ✅ Place Order View@login_required
def place_order_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    order_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total = product.price * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'total': total
            })
            total_price += total
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        last_order = None
        for item in order_items:
            order = Order.objects.create(
                user=request.user,
                customer_name=name,
                email=email,
                address=address,
                product=item['product'],
                quantity=item['quantity'],
                ordered_at=timezone.now()
            )
            last_order = order

        request.session['cart'] = {}

        if last_order:
            try:
                send_mail(
                    subject="Your ComfortZone Order Confirmation",
                    message=f"Thanks for your order!\nOrder ID: {last_order.order_id}\nWe’ll contact you soon.",
                    from_email='your_email@gmail.com',
                    recipient_list=[last_order.email],
                    fail_silently=True,
                )
            except:
                print("❌ Email failed")
            return redirect('order_success', order_id=last_order.order_id)

    return render(request, 'place_order.html', {
        'order_items': order_items,
        'total_price': total_price
    })

# ✅ My Orders@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'my_orders.html', {'orders': orders})

# ✅ Order Success Page
def order_success(request, order_id):
    return render(request, 'order_success.html', {'order_id': order_id})

# ✅ Optional Pages
def buy(request):
    return render(request, 'buy.html')

def cart(request):
    return redirect('cart_view')

# ✅ User Dashboard@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')
