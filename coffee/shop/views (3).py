from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Order, OrderProduct, Category, SliderItem, PurchaseRecord
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


def home(request:WSGIRequest):
    top_products = Product.objects.annotate(total_sold=Sum('orderproduct__quantity')).order_by('-total_sold')[:12]
    slider_items = SliderItem.objects.all()
    return render(request, 'shop/home.html', {'products': top_products, 'slider_items': slider_items})

def login_view(request:WSGIRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            return redirect('home')
        else:
            return render(request, 'shop/login.html', {'error': 'Invalid credentials'})
    return render(request, 'shop/login.html')

def register_view(request:WSGIRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        full_name = request.POST['full_name']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = full_name.split()[0]
            user.last_name = ' '.join(full_name.split()[1:])
            user.save()
            return redirect('login')
        else:
            return render(request, 'shop/register.html', {'error': 'Username already exists'})
    return render(request, 'shop/register.html')

def logout_view(request:WSGIRequest):
    logout(request)
    return redirect('home')

def product_page(request):
    vertical = request.GET.get('vertical', 'همه')
    if vertical == 'همه':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__name=vertical)
    categories = Category.objects.exclude(name='Default Category')
    return render(request, 'shop/products.html', {'products': products, 'selected_vertical': vertical, 'categories': categories})


@login_required
def cart(request:WSGIRequest):
    cart_order = Order.objects.filter(user=request.user, type='cart').first()
    cart_items = []
    total = 0
    if cart_order:
        for item in OrderProduct.objects.filter(order=cart_order):
            item_total = item.product.price * item.quantity
            cart_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.product.price,
                'item_total': item_total,
                'id': item.id
            })
            total += item_total
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.can_be_purchased(quantity):
        order, created = Order.objects.get_or_create(user=request.user, type='cart')
        order_product, created_ = OrderProduct.objects.get_or_create(order=order, product=product)
        if not created_:
            order_product.quantity += quantity
        else:
            order_product.quantity = quantity
        order_product.save()

        for product_ingredient in product.productingredient_set.all():
            product_ingredient.storage.amount -= product_ingredient.amount * quantity
            product_ingredient.storage.save()

        messages.success(request, 'با موفقیت اضافه شد.')
    else:
        available_quantity = product.max_purchase_quantity()
        messages.warning(request, f'محصولات اولیه به اندازه کافی موجود نیست. فقط میتوانید {available_quantity} واحد اضافه کنید.')
    return redirect('cart')

@login_required
def remove_from_cart(request, order_product_id):
    order_product = get_object_or_404(OrderProduct, id=order_product_id, order__user=request.user)

    product = order_product.product
    quantity = order_product.quantity
    for product_ingredient in product.productingredient_set.all():
        product_ingredient.storage.amount += product_ingredient.amount * quantity
        product_ingredient.storage.save()

    order_product.delete()
    return redirect('cart')

@login_required
def purchase_history(request):
    user = request.user
    orders = Order.objects.filter(user=user, type='completed').order_by('-created_at')
    
    order_details = []
    for order in orders:
        total_amount = sum(
            item.product.price * item.quantity for item in OrderProduct.objects.filter(order=order)
        )
        order.purchase_amount = total_amount
        order_details.append(order)
    
    return render(request, 'shop/purchase_history.html', {'orders': order_details})


def get_categories(request):
    categories = Category.objects.exclude(name='Default Category')
    categories_list = [{'name': 'همه'}]+list(categories.values('name'))
    return JsonResponse(categories_list, safe=False)


@login_required
def proceed_to_checkout(request):
    user = request.user
    try:
        order = Order.objects.get(user=user, type='cart')
    except Order.DoesNotExist:
        return redirect('cart')
    
    total_price = 0
    product_details = []
    
    for order_product in OrderProduct.objects.filter(order=order):
        product = order_product.product
        total_price += product.price * order_product.quantity
        print(product.price, type(product.price))
        product_details.append({
            'name': product.name,
            'quantity': order_product.quantity,
            'price': float(product.price),
        })

    delivery_type = request.POST.get('delivery_type', 'in_person')
    
    PurchaseRecord.objects.create(
        user=user,
        products=json.dumps(product_details),
        total_price=total_price,
    )
    
    order.type = 'completed'
    order.delivery_type = delivery_type
    order.save()
    return redirect('purchase_history')

 
@user_passes_test(lambda u: u.is_superuser)
def sales_chart_view(request):
    interval = request.GET.get('interval', 'monthly')
    selected_product = request.GET.get('product', 'all')
    
    products = Product.objects.all()
    sales_data = OrderProduct.objects.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('product__name')
    
    if selected_product != 'all':
        sales_data = sales_data.filter(product_id=selected_product)
    
    sales_data_list = list(sales_data)
    sales_data_json = json.dumps(sales_data_list, cls=DjangoJSONEncoder)

    context = {
        'sales_data': sales_data_json,
        'interval': interval,
        'products': products,
        'selected_product': int(selected_product) if selected_product != 'all' else 'all',
    }
    return render(request, 'shop/sales_chart.html', context)