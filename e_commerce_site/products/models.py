from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    
    # Add gender field for clothing categories
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('unisex', 'Unisex'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    # Clothing Categories
    CLOTHING_TYPES = [
        # 🟢 Men's Clothing
        ('mens_tshirt', 'Men\'s T-Shirt'),
        ('mens_shirt', 'Men\'s Shirt'),
        ('mens_trouser', 'Men\'s Trouser'),
        ('mens_jeans', 'Men\'s Jeans'),
        ('mens_kurta', 'Men\'s Kurta'),
        ('mens_shalwar', 'Men\'s Shalwar Kameez'),
        ('mens_waistcoat', 'Men\'s Waistcoat'),
        ('mens_blazer', 'Men\'s Blazer'),
        ('mens_suit', 'Men\'s Suit'),
        ('mens_hoodie', 'Men\'s Hoodie'),
        ('mens_jacket', 'Men\'s Jacket'),
        ('mens_coat', 'Men\'s Coat'),
        ('mens_short', 'Men\'s Shorts'),
        ('mens_shoes', 'Men\'s Shoes'),
        ('mens_sweater', 'Men\'s Sweater'),
        
        # 🟢 Women's Clothing
        ('womens_kurta', 'Women\'s Kurta'),
        ('womens_suit', 'Women\'s Suit'),
        ('womens_dress', 'Women\'s Dress'),
        ('womens_abaya', 'Women\'s Abaya'),
        ('womens_hoodie', 'Women\'s Hoodie'),
        ('womens_trouser', 'Women\'s Trouser'),
        ('womens_jeans', 'Women\'s Jeans'),
        ('womens_blouse', 'Women\'s Blouse'),
        ('womens_shawl', 'Women\'s Shawl'),
        ('womens_jacket', 'Women\'s Jacket'),
        ('womens_coat', 'Women\'s Coat'),
        ('womens_skirt', 'Women\'s Skirt'),
        ('womens_sweater', 'Women\'s Sweater'),
        ('womens_shoes', 'Women\'s Shoes'),
        
        # 🟢 Kids Clothing
        ('kids_kurta', 'Kids Kurta'),
        ('kids_tshirt', 'Kids T-Shirt'),
        ('kids_trouser', 'Kids Trouser'),
        ('kids_dress', 'Kids Dress'),
        ('kids_traditional', 'Kids Traditional Wear'),
        ('kids_jeans', 'Kids Jeans'),
        ('kids_hoodie', 'Kids Hoodie'),
        ('kids_jacket', 'Kids Jacket'),
        ('kids_coat', 'Kids Coat'),
        ('kids_shoes', 'Kids Shoes'),
    
    ]
    
    # Fabric Types for Pakistani Clothing
    FABRIC_TYPES = [
        # 🟢 COTTON & BLENDS (Most Popular in Pakistan)
        ('khadar', 'Khadar Cotton'),
        ('cotton', 'Pure Cotton'),
        ('linen', 'Linen'),
        ('cotton_linen', 'Cotton Linen Blend'),
        ('viscose', 'Viscose'),
        ('poly_cotton', 'Poly Cotton'),
        
        # 🟡 PREMIUM FABRICS
        ('silk', 'Pure Silk'),
        ('silk_cotton', 'Silk Cotton Blend'),
        ('chiffon', 'Chiffon'),
        ('georgette', 'Georgette'),
        ('organza', 'Organza'),
        
        # 🔴 LUXURY & TRADITIONAL
        ('banarsi', 'Banarsi Silk'),
        ('jamawar', 'Jamawar'),
        ('kashmiri', 'Kashmiri Wool'),
        ('pashmina', 'Pashmina'),
        ('embroidered', 'Embroidered Fabric'),
        
        # 🟣 DENIM & CASUAL
        ('denim', 'Denim'),
        ('corduroy', 'Corduroy'),
        ('terry_cotton', 'Terry Cotton'),
        ('jersey', 'Jersey'),
        ('fleece', 'Fleece'),
    ]
    
    # Size Choices
    SIZE_CHOICES = [
        # Standard Sizes
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        
        # Numeric Sizes
        ('28', '28'),
        ('30', '30'),
        ('32', '32'),
        ('34', '34'),
        ('36', '36'),
        ('38', '38'),
        ('40', '40'),
        ('42', '42'),
        ('44', '44'),
        
        # Kids Sizes
        ('2-3y', '2-3 Years'),
        ('4-5y', '4-5 Years'),
        ('6-7y', '6-7 Years'),
        ('8-9y', '8-9 Years'),
        ('10-12y', '10-12 Years'),
    ]
    
    # Color Choices
    COLOR_CHOICES = [
        ('white', 'White'),
        ('black', 'Black'),
        ('navy_blue', 'Navy Blue'),
        ('sky_blue', 'Sky Blue'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('gray', 'Gray'),
        ('brown', 'Brown'),
        ('beige', 'Beige'),
        ('maroon', 'Maroon'),
        ('olive', 'Olive'),
        ('teal', 'Teal'),
        ('multi', 'Multi Color'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=30, choices=CLOTHING_TYPES, default='mens_tshirt')
    image = models.ImageField(upload_to='Products/', blank=True)
    fabric_type = models.CharField(max_length=20, choices=FABRIC_TYPES, blank=True, null=True)
    
    # Size and Color
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=15, choices=COLOR_CHOICES, blank=True, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=50, unique=True)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Clothing-specific dimensions
    length = models.DecimalField(max_digits=6, decimal_places=2, help_text="Length in inches", blank=True, null=True)
    chest_width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Chest width in inches", blank=True, null=True)
    waist_width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Waist width in inches", blank=True, null=True)
    shoulder_width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Shoulder width in inches", blank=True, null=True)
    
    # Care instructions
    care_instructions = models.TextField(blank=True, help_text="Washing and care instructions")
    
    # New fields for clothing-specific attributes
    season = models.CharField(max_length=20, choices=[
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('all_season', 'All Season'),
        ('spring', 'Spring'),
        ('autumn', 'Autumn'),
    ], default='all_season')
    
    occasion = models.CharField(max_length=20, choices=[
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        ('wedding', 'Wedding'),
        ('eid', 'Eid'),
        ('everyday', 'Everyday Wear'),
    ], default='casual')
    
    # International sales fields
    origin_country = models.CharField(max_length=100, blank=True, default="Pakistan")
    available_domestic = models.BooleanField(default=True)
    available_international = models.BooleanField(default=False)
    export_allowed = models.BooleanField(default=False, help_text="Allow export/sale outside origin country")
    min_order_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], help_text="Minimum order quantity")
    lead_time_days = models.IntegerField(default=7, validators=[MinValueValidator(0)], help_text="Lead time in days")
    hs_code = models.CharField(max_length=32, blank=True, help_text="HS / Tariff code for export")
    is_customizable = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    def __str__(self):
        return f"{self.name} - {self.get_color_display()} - {self.get_size_display()}"
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    def get_discount_percentage(self):
        if self.compare_price and self.compare_price > self.price:
            return int(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    def get_gender(self):
        """Extract gender from product type"""
        if self.product_type.startswith('mens_'):
            return 'Men'
        elif self.product_type.startswith('womens_'):
            return 'Women'
        elif self.product_type.startswith('kids_'):
            return 'Kids'
        else:
            return 'Unisex'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Color variant for the image
    color_variant = models.CharField(max_length=15, choices=Product.COLOR_CHOICES, blank=True)
    
    def __str__(self):
        return f"Image for {self.product.name} - {self.color_variant if self.color_variant else 'Default'}"