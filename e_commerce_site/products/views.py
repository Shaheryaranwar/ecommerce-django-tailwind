from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Product, Category

# def product_list(request , categore_slug):
#     products = Product.objects.filter(is_active=True)
    
#     # Filtering
#     category_slug = request.GET.get('category')
#     wood_type = request.GET.get('wood_type')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')
    
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
    
#     if wood_type:
#         products = products.filter(wood_type=wood_type)
    
#     if min_price:
#         products = products.filter(price__gte=min_price)
    
#     if max_price:
#         products = products.filter(price__lte=max_price)
    
#     # Search
#     search_query = request.GET.get('search')
#     if search_query:
#         products = products.filter(
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query) |
#             Q(wood_type__icontains=search_query)
#         )
    
#     # Sorting
#     sort_by = request.GET.get('sort', 'name')
#     if sort_by == 'price_low':
#         products = products.order_by('price')
#     elif sort_by == 'price_high':
#         products = products.order_by('-price')
#     elif sort_by == 'newest':
#         products = products.order_by('-created_at')
#     else:
#         products = products.order_by('name')
    
#     context = {
#         'products': products,
#         'categories': Category.objects.filter(is_active=True),
#     }
#     return render(request, 'products/product_list.html', context)


# def product_detail(request, id,slug):
#     product = get_object_or_404(Product, slug=slug, is_active=True, id=id)
#     related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
#     context = {
#         'product': product,
#         'related_products': related_products,
#     }
#     return render(request, 'products/product_detail.html',{ 'product': product, 'related_products': related_products })
from .models import Product, Category

def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True)
    category = None

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "products/product_list.html", context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    return render(request, 'products/products/detail.html', {'product': product})

def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category.html', {
        'category': category,
        'products': products
    })