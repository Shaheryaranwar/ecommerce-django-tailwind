from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, render

from categories.models import Category
from core.models import HeroSlide, SiteSection
from products.models import Product

TESTIMONIALS = [
    {
        "name": "Ayesha R.",
        "city": "Lahore",
        "text": "The walnut dining set transformed our home. Craftsmanship you simply don't find in imported flat-pack furniture.",
    },
    {
        "name": "Bilal K.",
        "city": "Karachi",
        "text": "Ordered a sofa on Monday, delivered on Thursday. The team even assembled it in our living room.",
    },
    {
        "name": "Sana M.",
        "city": "Islamabad",
        "text": "Beautiful, solid wood pieces at honest prices. Aangan Living is now our first stop for every room.",
    },
]


def _active_products():
    return Product.objects.filter(
        is_active=True, status="published"
    ).select_related("category", "brand").prefetch_related("images", "variants")


def home(request):
    if request.method == "POST" and request.POST.get("newsletter_email"):
        messages.success(request, "You're on the list! Welcome to the Aangan Living family.")
        return redirect("core:home")

    hero_slides = HeroSlide.objects.filter(is_active=True).order_by("sort_order", "id")
    sections = []
    for section in SiteSection.objects.filter(is_active=True).order_by(
        "sort_order", "id"
    ):
        entry = {"key": section.key, "title": section.title, "type": section.section_type}
        if section.section_type == SiteSection.SectionType.HERO:
            entry["slides"] = hero_slides
        elif section.section_type == SiteSection.SectionType.FEATURED_CATEGORIES:
            categories = list(
                Category.objects.filter(is_active=True, is_featured=True).order_by(
                    "sort_order"
                )[:6]
            )
            if not categories:
                continue
            entry["categories"] = categories
        elif section.section_type == SiteSection.SectionType.TRENDING_PRODUCTS:
            products = _active_products().filter(is_bestseller=True)[:8]
            if not products:
                continue
            entry["products"] = products
        elif section.section_type == SiteSection.SectionType.SPOTLIGHT:
            product = (
                _active_products().filter(is_spotlight=True).first()
                or _active_products().filter(is_featured=True).first()
            )
            if not product:
                continue
            entry["product"] = product
        elif section.section_type == SiteSection.SectionType.PROMO:
            entry["delivery_threshold"] = settings.FREE_DELIVERY_THRESHOLD
        sections.append(entry)

    context = {
        "sections": sections,
        "featured_products": _active_products().filter(is_featured=True)[:8],
        "new_arrivals": _active_products().filter(is_new=True)[:8],
        "testimonials": TESTIMONIALS,
    }
    return render(request, "home/index.html", context)


def search(request):
    query = request.GET.get("q", "").strip()
    products = []
    if query:
        products = (
            _active_products()
            .filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(short_description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(brand__name__icontains=query)
                | Q(material__icontains=query)
            )
            .distinct()
        )
    return render(
        request,
        "products/search.html",
        {"query": query, "products": products},
    )


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")
        if name and email and message:
            send_mail(
                subject=f"Contact form — {name}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=None,
                recipient_list=["care@aanganliving.pk"],
                fail_silently=True,
            )
            messages.success(request, "Thank you! Our team will get back to you within 24 hours.")
        else:
            messages.error(request, "Please fill in all fields.")
        return redirect("core:contact")
    return render(request, "core/contact.html")
