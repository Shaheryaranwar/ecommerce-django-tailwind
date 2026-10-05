from django.core.paginator import Paginator
from django.db.models import Min, Q
from django.shortcuts import get_object_or_404, render

from categories.models import Category

from .models import AttributeValue, Brand, Product

SORT_OPTIONS = {
    "featured": ("-is_featured", "-created_at"),
    "newest": ("-created_at",),
    "price_asc": ("min_price",),
    "price_desc": ("-min_price",),
    "name": ("name",),
}

MATERIALS = [choice[0] for choice in Product.MATERIAL_CHOICES]


def _query_string(request):
    params = request.GET.copy()
    params.pop("page", None)
    return params.urlencode()


def _build_queryset(request, base_qs=None):
    qs = (base_qs or Product.objects).filter(is_active=True, status="published")
    qs = qs.select_related("category", "brand").prefetch_related("images", "variants")

    # search
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(brand__name__icontains=query)
        ).distinct()

    # category (includes children)
    category_slug = request.GET.get("category")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        qs = qs.filter(category_id__in=category.descendant_ids())

    # material
    materials = request.GET.getlist("material")
    if materials:
        qs = qs.filter(material__in=materials)

    # brand
    brands = request.GET.getlist("brand")
    if brands:
        qs = qs.filter(brand__slug__in=brands)

    # price range (applied on the cheapest active variant)
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    qs = qs.annotate(min_price=Min("variants__price"))
    if min_price:
        qs = qs.filter(min_price__gte=min_price)
    if max_price:
        qs = qs.filter(min_price__lte=max_price)

    # in-stock only
    if request.GET.get("in_stock"):
        qs = qs.filter(variants__stock__gt=0).distinct()

    # sorting
    sort = request.GET.get("sort", "featured")
    qs = qs.order_by(*SORT_OPTIONS.get(sort, SORT_OPTIONS["featured"]))

    if request.GET.get("is_new"):
        qs = qs.filter(is_new=True)
    if request.GET.get("on_sale"):
        qs = qs.filter(variants__compare_price__isnull=False).distinct()

    return qs, category_slug or None


def product_list(request):
    qs, active_category_slug = _build_queryset(request)
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "products": page,
        "pagination": page,
        "query_string": _query_string(request),
        "categories": Category.objects.filter(is_active=True, parent__isnull=True)
        .prefetch_related("children")
        .order_by("sort_order", "name"),
        "brands": Brand.objects.filter(is_active=True),
        "materials": MATERIALS,
        "active_category_slug": active_category_slug,
        "current_sort": request.GET.get("sort", "featured"),
        "filters": {
            "materials": request.GET.getlist("material"),
            "brands": request.GET.getlist("brand"),
            "min_price": request.GET.get("min_price", ""),
            "max_price": request.GET.get("max_price", ""),
            "in_stock": request.GET.get("in_stock", ""),
        },
        "page_title": "Shop All Furniture",
    }
    if request.GET.get("is_new"):
        context["page_title"] = "New Arrivals"
    if request.GET.get("on_sale"):
        context["page_title"] = "Sale"
    return render(request, "products/product_list.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    qs, _ = _build_queryset(
        request, Product.objects.filter(category_id__in=category.descendant_ids())
    )
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))

    context = {
        "category": category,
        "products": page,
        "pagination": page,
        "query_string": _query_string(request),
        "categories": Category.objects.filter(is_active=True, parent__isnull=True)
        .prefetch_related("children")
        .order_by("sort_order", "name"),
        "brands": Brand.objects.filter(is_active=True),
        "materials": MATERIALS,
        "current_sort": request.GET.get("sort", "featured"),
        "filters": {
            "materials": request.GET.getlist("material"),
            "brands": request.GET.getlist("brand"),
            "min_price": request.GET.get("min_price", ""),
            "max_price": request.GET.get("max_price", ""),
            "in_stock": request.GET.get("in_stock", ""),
        },
    }
    return render(request, "products/category.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category", "brand").prefetch_related(
            "images", "variants__attribute_values__attribute"
        ),
        slug=slug,
        is_active=True,
        status="published",
    )
    related = (
        Product.objects.filter(
            category=product.category, is_active=True, status="published"
        )
        .exclude(id=product.id)
        .select_related("category")
        .prefetch_related("images", "variants")[:4]
    )
    reviews = product.reviews.filter(is_approved=True).select_related("user")
    user_review = None
    if request.user.is_authenticated:
        user_review = product.reviews.filter(user=request.user).first()

    attribute_groups = []
    for value in (
        AttributeValue.objects.filter(variants__product=product)
        .select_related("attribute")
        .distinct()
        .order_by("attribute__name", "value")
    ):
        if not attribute_groups or attribute_groups[-1]["attribute"] != value.attribute:
            attribute_groups.append({"attribute": value.attribute, "values": []})
        attribute_groups[-1]["values"].append(value)

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "first_variant": product.variants.filter(is_active=True).first(),
            "attribute_groups": attribute_groups,
            "related": related,
            "reviews": reviews,
            "user_review": user_review,
            "rating_data": product.average_rating,
        },
    )
