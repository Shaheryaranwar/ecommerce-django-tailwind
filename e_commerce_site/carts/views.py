from django.shortcuts import render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.views.decorators import require_POST, require_http_methods
from django.http import JsonResponse

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart_id = request.session.get("cart_id")
   
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    response_data = {'success': True, "message": f'Added {product.name} to cart', 'cart_item_count': cart.items.count()}
    return JsonResponse(response_data)

def cart_detail(request):
    cart_id = request.session.get("cart_id")
    cart = None
    if cart_id:
        try:
            cart = get_object_or_404(Cart, id=cart_id) 
        except Cart.DoesNotExist:
            cart = None
    return render(request, 'carts/cart_detail.html', {'cart': cart})    