"""Seed the Aangan Living catalog with categories, brands and products.

Usage:
    python manage.py seed_catalog
"""

import random
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from categories.models import Category
from products.models import Attribute, AttributeValue, Brand, Product, ProductImage, ProductVariant
from reviews.models import Review

IMG = "https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=900&q=80"

CATEGORIES = [
    {
        "slug": "living-room",
        "name": "Living Room",
        "description": "Sofas, chairs and tables that anchor the heart of your home.",
        "image": "1522708323590-d24dbb6b0267",
        "children": [
            ("sofas", "Sofas", "1538688525198-9b88f6f53126"),
            ("lounge-chairs", "Lounge Chairs", "1567538096630-e0c55bd6374c"),
            ("coffee-tables", "Coffee Tables", "1533090481720-856c6e3c1fdc"),
            ("tv-units", "TV Units", "1618220179428-22790b461013"),
        ],
    },
    {
        "slug": "bedroom",
        "name": "Bedroom",
        "description": "Restful retreats — beds, wardrobes and storage in solid wood.",
        "image": "1567016432779-094069958ea5",
        "children": [
            ("beds", "Beds", "1505693416388-ac5ce068fe85"),
            ("wardrobes", "Wardrobes", "1560185007-cde436f6a4d0"),
            ("dressers", "Dressers", "1530018607912-eff2daa1bac4"),
            ("nightstands", "Nightstands", "1549187774-b4e9b0445b41"),
        ],
    },
    {
        "slug": "dining",
        "name": "Dining",
        "description": "Tables made for gatherings, feasts and long conversations.",
        "image": "1519710164239-da123dc03ef4",
        "children": [
            ("dining-tables", "Dining Tables", "1449247709967-d4461a6a6103"),
            ("dining-chairs", "Dining Chairs", "1499933374294-4584851497cc"),
            ("sideboards", "Sideboards", "1594026112284-02bb6f3352fe"),
        ],
    },
    {
        "slug": "office",
        "name": "Office",
        "description": "Focused, beautiful workspaces for home and studio.",
        "image": "1524758631624-e2822e304c36",
        "children": [
            ("desks", "Desks", "1550226891-ef816aed4a98"),
            ("office-chairs", "Office Chairs", "1507089947368-19c1da9775ae"),
            ("bookcases", "Bookcases", "1518455027359-f3f8164ba6bd"),
        ],
    },
    {
        "slug": "outdoor",
        "name": "Outdoor",
        "description": "Weather-ready rattan and teak for lawns and terraces.",
        "image": "1600585154340-be6161a56a0c",
        "children": [
            ("garden-sets", "Garden Sets", "1616627561950-9f746e330187"),
            ("loungers", "Loungers", "1600566753086-00f18fb6b3ea"),
        ],
    },
    {
        "slug": "decor",
        "name": "Décor",
        "description": "Lamps, mirrors, rugs and accents that finish a room.",
        "image": "1583847268964-b28dc8f51f92",
        "children": [
            ("lighting", "Lighting", "1507473885765-e6ed057f782c"),
            ("mirrors", "Mirrors", "1616594039964-ae9021a400a0"),
            ("rugs", "Rugs", "1600607687939-ce8a6c25118c"),
            ("accessories", "Accessories", "1513694203232-719a280e022f"),
        ],
    },
]

# (name, slug, country)
BRANDS = [
    ("Aangan Studio", "aangan-studio", "Pakistan"),
    ("Teak & Co", "teak-and-co", "Pakistan"),
    ("Sheesham House", "sheesham-house", "Pakistan"),
]

# (category_slug, name, slug, short, description, material, finish, dimensions,
#  images, price, compare, stock, flags, brand_slug)
PRODUCTS = [
    # ---------------- Living Room / Sofas ----------------
    ("sofas", "Mehrban 3-Seater Sofa", "mehrban-3-seater-sofa",
     "A low-slung silhouette in sun-washed linen with a solid teak base.",
     "The Mehrban is our most-loved sofa — deep seats, feather-wrapped cushions and a kiln-dried teak frame that carries a lifetime of evenings. Upholstered in premium linen with removable, washable covers.",
     "fabric", "Natural Linen", '84" W x 36" D x 30" H',
     ["1555041469-a586c61ea9bc", "1538688525198-9b88f6f53126", "1522708323590-d24dbb6b0267"],
     189000, 210000, 8, ["featured", "bestseller"], "aangan-studio"),
    ("sofas", "Dastaan Sectional Sofa", "dastaan-sectional-sofa",
     "A modular four-seat sectional that grows with your living room.",
     "Configure the Dastaan your way — left or right chaise, oak or walnut legs. Hand-stitched upholstery over high-resilience foam, with a solid sheesham frame.",
     "fabric", "Oat Bouclé", '104" W x 64" D x 31" H',
     ["1616486338812-3dadae4b4ace", "1519947486511-46149fa0a254"],
     279000, None, 4, ["featured", "new"], "aangan-studio"),
    ("sofas", "Sitara Love Seat", "sitara-love-seat",
     "Compact comfort for two, in rich forest velvet.",
     "A two-seater with presence — deep buttoned back, turned legs and cotton-velvet upholstery. Ideal for bedrooms, balconies and reading corners.",
     "velvet", "Forest Velvet", '62" W x 34" D x 31" H',
     ["1618220179428-22790b461013", "1493663284031-b7e3aefcae8e"],
     129000, 145000, 6, [], "teak-and-co"),
    ("sofas", "Zameen Corner Sofa", "zameen-corner-sofa",
     "A family-sized corner sofa in warm terracotta weave.",
     "Built for large gatherings — reinforced joinery, stain-resistant weave and a frame guaranteed for five years. Seats six comfortably.",
     "fabric", "Terracotta Weave", '110" W x 72" D x 30" H',
     ["1554295405-abb8fd54f153", "1522708323590-d24dbb6b0267"],
     315000, None, 3, ["bestseller"], "aangan-studio"),

    # ---------------- Lounge Chairs ----------------
    ("lounge-chairs", "Gul Lounge Chair", "gul-lounge-chair",
     "A sculpted lounge chair inspired by the curve of a gulab petal.",
     "Moulded teak shell with a hand-woven cane back and plush seat cushion. A statement piece that cradles as beautifully as it looks.",
     "wood", "Natural Teak", '30" W x 32" D x 31" H',
     ["1567538096630-e0c55bd6374c", "1507089947368-19c1da9775ae"],
     84000, None, 9, ["featured", "new"], "aangan-studio"),
    ("lounge-chairs", "Raat Accent Chair", "raat-accent-chair",
     "Midnight upholstery, golden sheesham legs — quiet drama.",
     "A deep, enveloping seat wrapped in charcoal chenille. The contrast of dark fabric and warm wood makes it the focal point of any room.",
     "fabric", "Charcoal Chenille", '29" W x 31" D x 33" H',
     ["1540574163026-643ea20ade25", "1592078615290-033ee584e267"],
     74000, 82000, 7, [], "sheesham-house"),
    ("lounge-chairs", "Chand Rocking Chair", "chand-rocking-chair",
     "A hand-carved walnut rocker for slow evenings.",
     "Gentle rock, hand-oiled walnut and a woven rush seat. Made by artisans in Chiniot who have carved rockers for three generations.",
     "wood", "Walnut", '26" W x 34" D x 40" H',
     ["1598300042247-d088f8ab3a91", "1540932239986-30128078f3c5"],
     69000, None, 5, ["new"], "aangan-studio"),

    # ---------------- Coffee Tables ----------------
    ("coffee-tables", "Sangam Coffee Table", "sangam-coffee-table",
     "Where marble meets mango wood — our signature centre table.",
     "A honed white marble top resting on a solid mango-wood base. Every table has its own veining, so no two are alike.",
     "mixed", "White Marble / Mango Wood", '48" W x 26" D x 16" H',
     ["1533090481720-856c6e3c1fdc", "1518455027359-f3f8164ba6bd"],
     56000, None, 10, ["featured", "bestseller"], "aangan-studio"),
    ("coffee-tables", "Darya Nesting Tables", "darya-nesting-tables",
     "A pair of nesting tables in smoked oak and brass.",
     "Tuck the smaller beneath the larger, or pull them apart for guests. Brushed brass inlay traces the grain of the smoked oak.",
     "wood", "Smoked Oak", '38" W x 20" D x 18" H',
     ["1518455027359-f3f8164ba6bd", "1533090481720-856c6e3c1fdc"],
     42500, None, 12, [], "teak-and-co"),
    ("coffee-tables", "Mitti Round Table", "mitti-round-table",
     "A solid teak round table with a soft, hand-rubbed finish.",
     "Perfect for compact living rooms. The rounded edges and low profile make it child-friendly and effortlessly elegant.",
     "wood", "Teak", '34" W x 34" D x 15" H',
     ["1595526114035-0d45ed16cfbf", "1518455027359-f3f8164ba6bd"],
     38000, 44000, 8, [], "aangan-studio"),

    # ---------------- TV Units ----------------
    ("tv-units", "Nazar TV Console", "nazar-tv-console",
     "A low-profile console with fluted doors and cable management.",
     "Walnut veneer over solid wood, soft-close doors and cut-outs that keep every cable hidden. Fits screens up to 75 inches.",
     "wood", "Walnut", '72" W x 18" D x 20" H',
     ["1618220179428-22790b461013", "1522708323590-d24dbb6b0267"],
     88000, None, 6, ["featured"], "aangan-studio"),
    ("tv-units", "Sheesham Media Wall", "sheesham-media-wall",
     "A full media wall with shelving, drawers and room for décor.",
     "Modular panels let you build around any screen size. Solid sheesham with iron accents and generous open shelving.",
     "wood", "Sheesham", '96" W x 16" D x 72" H',
     ["1615873968403-89e068629265", "1522708323590-d24dbb6b0267"],
     156000, 172000, 3, ["new"], "sheesham-house"),

    # ---------------- Beds ----------------
    ("beds", "Raunaq King Bed", "raunaq-king-bed",
     "A statement headboard of vertical teak slats — warm and architectural.",
     "Solid teak headboard with upholstered inserts, reinforced centre rail and hydraulic storage in the base. The bed your bedroom has been waiting for.",
     "wood", "Teak", '78" W x 84" L x 48" H',
     ["1505693416388-ac5ce068fe85", "1567016432779-094069958ea5", "1505691938895-1758d7feb511"],
     168000, 185000, 7, ["featured", "bestseller"], "aangan-studio"),
    ("beds", "Neend Queen Bed", "neend-queen-bed",
     "A low platform bed in pale oak for airy, modern bedrooms.",
     "Japanese-inspired low profile with a floating bedside shelf built into the headboard. Solid oak, finished with natural oil.",
     "wood", "Pale Oak", '66" W x 82" L x 30" H',
     ["1631049307264-da0ec9d70304", "1549187774-b4e9b0445b41"],
     142000, None, 5, ["new"], "teak-and-co"),
    ("beds", "Shabnam Upholstered Bed", "shabnam-upholstered-bed",
     "A fully upholstered bed in mist-grey linen with deep buttoning.",
     "Soft to lean against, solid underneath. The padded headboard makes late-night reading a pleasure.",
     "fabric", "Mist Grey Linen", '76" W x 85" L x 46" H',
     ["1616594039964-ae9021a400a0", "1505691938895-1758d7feb511"],
     154000, None, 4, [], "aangan-studio"),

    # ---------------- Wardrobes ----------------
    ("wardrobes", "Haveli Wardrobe", "haveli-wardrobe",
     "A four-door wardrobe with a carved border inspired by old havelis.",
     "Solid sheesham with hand-carved trim, cedar-lined drawers and soft-close hinges. Fitted with two hanging rails and six shelves.",
     "wood", "Sheesham", '84" W x 24" D x 84" H',
     ["1560185007-cde436f6a4d0", "1567016432779-094069958ea5"],
     198000, 220000, 3, ["featured"], "sheesham-house"),
    ("wardrobes", "Sukoon Sliding Wardrobe", "sukoon-sliding-wardrobe",
     "Mirrored sliding doors that make small rooms feel twice as large.",
     "Full-height mirrors, felt-lined jewellery trays and a motion-sensor light inside. Engineered to glide silently for years.",
     "wood", "White Oak", '78" W x 24" D x 90" H',
     ["1583847268964-b28dc8f51f92", "1567016432779-094069958ea5"],
     235000, None, 2, ["bestseller"], "aangan-studio"),

    # ---------------- Dressers ----------------
    ("dressers", "Aaina Dresser", "aaina-dresser",
     "A nine-drawer dresser with a round mirror and brass pulls.",
     "Deep drawers on soft-close runners, a tilting mirror and a jewellery tray in the top drawer. Walnut, hand-rubbed to a soft sheen.",
     "wood", "Walnut", '58" W x 20" D x 34" H',
     ["1530018607912-eff2daa1bac4", "1549187774-b4e9b0445b41"],
     112000, None, 5, [], "aangan-studio"),

    # ---------------- Nightstands ----------------
    ("nightstands", "Raat Ki Mez", "raat-ki-mez",
     "A compact nightstand with a hidden phone-charging drawer.",
     "Solid oak with a soft-close drawer, open shelf and a discreet cable port. The USB port inside the drawer keeps phones out of sight.",
     "wood", "Oak", '20" W x 16" D x 22" H',
     ["1549187774-b4e9b0445b41", "1505693416388-ac5ce068fe85"],
     24000, None, 15, ["new"], "teak-and-co"),

    # ---------------- Dining Tables ----------------
    ("dining-tables", "Dastarkhwan Dining Table", "dastarkhwan-dining-table",
     "An eight-seater teak table — the centrepiece of every feast.",
     "A single slab-inspired top of joined teak over trestle legs. Seats eight comfortably, ten at a squeeze. Built for Eid lunches and Sunday breakfasts alike.",
     "wood", "Teak", '84" W x 40" D x 30" H',
     ["1519710164239-da123dc03ef4", "1499933374294-4584851497cc", "1449247709967-d4461a6a6103"],
     148000, 165000, 6, ["featured", "bestseller"], "aangan-studio"),
    ("dining-tables", "Bagh Round Table", "bagh-round-table",
     "A four-seater round table in mango wood with a pedestal base.",
     "Compact and convivial — the round top keeps conversation flowing. Finished with a food-safe matte lacquer.",
     "wood", "Mango Wood", '48" W x 48" D x 30" H',
     ["1449247709967-d4461a6a6103", "1519710164239-da123dc03ef4"],
     84000, None, 7, [], "aangan-studio"),
    ("dining-tables", "Sang-e-Marmar Dining Table", "sang-e-marmar-dining-table",
     "A marble-topped table for those who love to host in style.",
     "Polished marble over a blackened metal base. Seats six. Each slab is sealed against stains before it leaves the workshop.",
     "marble", "Polished Marble", '72" W x 38" D x 30" H',
     ["1551298370-9d3d53740c72", "1484154218962-a197022b5858"],
     178000, None, 4, ["new"], "aangan-studio"),

    # ---------------- Dining Chairs ----------------
    ("dining-chairs", "Baithak Dining Chair", "baithak-dining-chair",
     "A woven-cane dining chair with a gently curved back.",
     "Solid oak frame, hand-woven cane back and a linen seat cushion. Light enough to move, strong enough for decades.",
     "wood", "Oak / Cane", '19" W x 22" D x 34" H',
     ["1499933374294-4584851497cc", "1519710164239-da123dc03ef4"],
     22000, None, 40, ["bestseller"], "aangan-studio"),
    ("dining-chairs", "Sitara Dining Chair", "sitara-dining-chair",
     "Upholstered comfort for long dinners and longer conversations.",
     "A plush seat and curved back upholstered in performance fabric — spills wipe clean, comfort stays.",
     "fabric", "Sand Bouclé", '20" W x 23" D x 35" H',
     ["1586023492125-27b2c045efd7", "1499933374294-4584851497cc"],
     18500, 21500, 30, [], "aangan-studio"),

    # ---------------- Sideboards ----------------
    ("sideboards", "Ganj Sideboard", "ganj-sideboard",
     "Storage, beautifully solved — three doors, six shelves, one statement.",
     "Fluted walnut doors with brass pulls and an open display shelf. The workhorse of the dining room, dressed for a gallery.",
     "wood", "Walnut", '72" W x 18" D x 32" H',
     ["1594026112284-02bb6f3352fe", "1484154218962-a197022b5858"],
     118000, None, 5, ["featured"], "aangan-studio"),

    # ---------------- Desks ----------------
    ("desks", "Kaam Writing Desk", "kaam-writing-desk",
     "A clean-lined oak desk with two drawers and a cable tray.",
     "Designed for focus — deep enough for a monitor and notebooks, with drawers for the clutter. Solid oak with a matte lacquer finish.",
     "wood", "Oak", '55" W x 26" D x 30" H',
     ["1524758631624-e2822e304c36", "1550226891-ef816aed4a98"],
     64000, None, 9, ["featured", "new"], "aangan-studio"),
    ("desks", "Mehnat Standing Desk", "mehnat-standing-desk",
     "A walnut desk that lifts you from sitting to standing in seconds.",
     "Dual motors, memory presets and a solid walnut top. Your back will thank you, your office will envy you.",
     "wood", "Walnut", '60" W x 30" D x 48" H',
     ["1550226891-ef816aed4a98", "1524758631624-e2822e304c36"],
     132000, None, 4, ["bestseller"], "teak-and-co"),

    # ---------------- Office Chairs ----------------
    ("office-chairs", "Tasveer Office Chair", "tasveer-office-chair",
     "An ergonomic chair that doesn't look like office furniture.",
     "Adjustable lumbar, breathable mesh and a seat that tilts with you. Upholstered in charcoal with a chrome base.",
     "leather", "Charcoal Leather", '26" W x 26" D x 42" H',
     ["1507089947368-19c1da9775ae", "1592078615290-033ee584e267"],
     46000, 52000, 14, [], "aangan-studio"),
    ("office-chairs", "Ustaad Task Chair", "ustaad-task-chair",
     "Compact, supportive and quietly elegant in camel leather.",
     "A smaller footprint for home offices — but full adjustability where it matters. Stitched in top-grain camel leather.",
     "leather", "Camel Leather", '24" W x 24" D x 40" H',
     ["1592078615290-033ee584e267", "1507089947368-19c1da9775ae"],
     54000, None, 8, ["new"], "sheesham-house"),

    # ---------------- Bookcases ----------------
    ("bookcases", "Kitaab Bookcase", "kitaab-bookcase",
     "Five open shelves in solid oak — a library wall in miniature.",
     "Fixed shelves rated for heavy art books, with a recessed plinth. The open back keeps rooms feeling light.",
     "wood", "Oak", '36" W x 14" D x 72" H',
     ["1518455027359-f3f8164ba6bd", "1524758631624-e2822e304c36"],
     62000, None, 6, [], "aangan-studio"),
    ("bookcases", "Deevar Shelving System", "deevar-shelving-system",
     "A modular shelving system that grows with your collection.",
     "Blackened iron frame with adjustable oak shelves. Buy two and build a wall — connectors included.",
     "mixed", "Black Iron / Oak", '40" W x 16" D x 78" H',
     ["1573865526739-10659fec78a5", "1518455027359-f3f8164ba6bd"],
     88000, None, 4, ["new"], "teak-and-co"),

    # ---------------- Garden Sets ----------------
    ("garden-sets", "Baghicha Garden Set", "baghicha-garden-set",
     "A four-seat rattan set for lawn evenings and winter sun.",
     "Weather-resistant rattan weave over aluminium frames, with cream cushions in Sunbrella fabric. Includes sofa, two chairs and a table.",
     "rattan", "Natural Rattan", 'Sofa 78" W · Table 40" W',
     ["1616627561950-9f746e330187", "1600585154340-be6161a56a0c"],
     215000, 240000, 5, ["featured"], "aangan-studio"),
    ("garden-sets", "Chhat Garden Sofa", "chhat-garden-sofa",
     "A deep two-seater in dark resin weave — built for rooftops.",
     "UV-stabilised weave, quick-dry cushions and a frame that shrugs off monsoon and dust alike.",
     "rattan", "Espresso Weave", '64" W x 32" D x 30" H',
     ["1600566753086-00f18fb6b3ea", "1616627561950-9f746e330187"],
     124000, None, 4, [], "teak-and-co"),

    # ---------------- Loungers ----------------
    ("loungers", "Dhoop Lounger", "dhoop-lounger",
     "An adjustable teak lounger for slow afternoons by the lawn.",
     "Five recline positions, a sliding side table and solid teak that weathers to a beautiful silver over time.",
     "wood", "Teak", '26" W x 76" L x 14" H',
     ["1600566753086-00f18fb6b3ea", "1600607687920-4e2a09cf159d"],
     58000, None, 6, ["new"], "aangan-studio"),

    # ---------------- Lighting ----------------
    ("lighting", "Roshni Floor Lamp", "roshni-floor-lamp",
     "A sculptural floor lamp in brushed brass and linen shade.",
     "Warm, diffused light for reading corners. The weighted base keeps it steady on carpets and marble alike.",
     "metal", "Brushed Brass", '18" W x 60" H',
     ["1507473885765-e6ed057f782c", "1583847268964-b28dc8f51f92"],
     32000, None, 12, ["featured"], "aangan-studio"),
    ("lighting", "Chandni Pendant", "chandni-pendant",
     "A hand-blown glass pendant that pools light like moonlight.",
     "Hung over a dining table or island, the dimpled glass scatters soft shadows across the room. Dimmable with most LED bulbs.",
     "glass", "Blown Glass", '14" W x 12" H',
     ["1581244277943-fe4a9c777189", "1507473885765-e6ed057f782c"],
     26000, None, 10, ["new"], "teak-and-co"),

    # ---------------- Mirrors ----------------
    ("mirrors", "Aaina Arch Mirror", "aaina-arch-mirror",
     "A tall arch mirror with a slim brass frame — instant glamour.",
     "Lean it against the wall or hang it in the entry. The arch shape draws the eye up and makes ceilings feel taller.",
     "metal", "Brass", '30" W x 72" H',
     ["1616594039964-ae9021a400a0", "1583847268964-b28dc8f51f92"],
     44000, None, 8, ["featured"], "aangan-studio"),
    ("mirrors", "Dhundh Round Mirror", "dhundh-round-mirror",
     "A minimal round mirror framed in natural oak.",
     "Unfussy and warm — works in bathrooms, bedrooms and hallways. Mounting hardware included.",
     "wood", "Oak", '28" W x 28" H',
     ["1513694203232-719a280e022f", "1560448204-e02f11c3d0e2"],
     28000, 32000, 12, [], "sheesham-house"),

    # ---------------- Rugs ----------------
    ("rugs", "Gulistan Rug", "gulistan-rug",
     "A hand-tufted wool rug in faded terracotta and cream.",
     "Traditional motifs, contemporary palette. Hand-tufted in wool with a cotton backing — soft underfoot and easy to live with.",
     "fabric", "Wool", '6\' x 9\'',
     ["1600607687939-ce8a6c25118c", "1522708323590-d24dbb6b0267"],
     68000, None, 7, ["featured"], "aangan-studio"),
    ("rugs", "Sehra Runner", "sehra-runner",
     "A flatweave runner for hallways, in sand and charcoal stripes.",
     "Handwoven cotton flatweave — thin enough for doors to clear, tough enough for the busiest corridor in the house.",
     "fabric", "Cotton", '2.5\' x 8\'',
     ["1600607687920-4e2a09cf159d", "1600607687939-ce8a6c25118c"],
     24000, None, 15, ["new"], "teak-and-co"),

    # ---------------- Accessories ----------------
    ("accessories", "Khazana Chest", "khazana-chest",
     "A small brass-bound chest for blankets, toys or secrets.",
     "Solid sheesham with hand-beaten brass corners and a soft-close lid. Doubles as a coffee table in compact rooms.",
     "wood", "Sheesham / Brass", '30" W x 18" D x 18" H',
     ["1584100936595-c0654b55a2e2", "1513694203232-719a280e022f"],
     36000, None, 9, [], "sheesham-house"),
    ("accessories", "Dastarkhwan Serving Tray", "dastarkhwan-serving-tray",
     "A carved mango-wood tray for chai, dessert or display.",
     "Food-safe oil finish, brass handles and enough room for eight cups of chai. The host's secret weapon.",
     "wood", "Mango Wood", '20" W x 14" D x 2" H',
     ["1610701596007-11502861dcfa", "1449247709967-d4461a6a6103"],
     9500, None, 30, ["bestseller"], "aangan-studio"),
    ("accessories", "Nakshi Cushion Pair", "nakshi-cushion-pair",
     "A pair of block-printed cushions in indigo and ivory.",
     "Hand block-printed cotton, feather-filled and finished with hidden zips. The easiest way to refresh a sofa.",
     "fabric", "Cotton", '18" x 18" (each)',
     ["1600607687939-ce8a6c25118c", "1493663284031-b7e3aefcae8e"],
     8500, None, 50, ["new"], "aangan-studio"),
]

DEMO_REVIEWS = [
    ("mehrban-3-seater-sofa", 5, "Worth every rupee",
     "Three months in and the sofa still looks brand new. Delivery team assembled it in 20 minutes and took all the packing away."),
    ("mehrban-3-seater-sofa", 4, "Beautiful, seats slightly firm",
     "Gorgeous linen and solid frame. Cushions took a couple of weeks to soften up but now it's perfect."),
    ("dastarkhwan-dining-table", 5, "The heart of our home",
     "We hosted both Eids on this table. Solid teak, zero wobble, and the finish survived three kids."),
    ("raunaq-king-bed", 5, "Sleeps like a hotel",
     "No creaks, no movement. The hydraulic storage fits all our winter blankets. Delivery to Karachi took 6 days."),
    ("sangam-coffee-table", 4, "Unique marble top",
     "The veining on ours is stunning. One star off because it's heavy to move — but that's solid wood for you."),
    ("baithak-dining-chair", 5, "Bought six, ordering six more",
     "Light, sturdy and the cane back is beautiful. Our dining room finally looks finished."),
]

DEMO_PROJECTS = [
    {
        "title": "Our walnut dining room glow-up",
        "category": "styling",
        "status": "approved",
        "description": (
            "We moved into a new house with a plain white dining room and it never felt like home. "
            "After a lot of Pinterest scrolling we landed on a warm walnut and cream palette. "
            "We swapped the plastic chairs for solid wood ones, added a handwoven runner and hung "
            "a pair of brass pendants low over the table. The biggest lesson: lighting changes "
            "everything — warm bulbs at 2700K made the wood glow. Total cost was under Rs 150,000 "
            "including the table, and the room is now where everyone gathers."
        ),
        "images": ["1519710164239-da123dc03ef4", "1615873968403-89e068629265"],
    },
    {
        "title": "Restoring a 40-year-old sheesham jhoola",
        "category": "restoration",
        "status": "approved",
        "description": (
            "This swing belonged to my grandmother and had been sitting in storage for a decade, "
            "cracked, faded and creaky. Over six weekends I sanded it down to bare wood, filled "
            "the cracks with wood filler, and refinished it with three coats of Danish oil. "
            "I learned how to identify sheesham grain, why you should never rush drying between "
            "coats, and how to re-rope the seat properly. It now hangs in our veranda and my "
            "grandmother cried when she saw it. Restoration is 80% patience and 20% sandpaper."
        ),
        "images": ["1538688525198-9b88f6f53126", "1555041469-a586c61ea9bc"],
    },
    {
        "title": "DIY pegboard study wall",
        "category": "diy",
        "status": "approved",
        "description": (
            "Working from home meant my desk was drowning in cables, notes and stationery. "
            "I built a full-wall pegboard system from two plywood sheets, some primer and paint. "
            "First time using a jigsaw and a pocket-hole jig — both are now my favourite tools. "
            "Total material cost was about Rs 18,000 and a weekend. Pro tip: paint the pegboard "
            "before drilling the holes into the wall, and use spacers so the pegs actually fit."
        ),
        "images": ["1524758631624-e2822e304c36"],
    },
    {
        "title": "Monsoon-proofing the veranda lounge",
        "category": "makeover",
        "status": "approved",
        "description": (
            "Our outdoor lounge looked beautiful for exactly two months before the monsoon ruined "
            "the cushions. This time we built for the weather: teak frames, quick-dry foam, "
            "sunbrella-style covers and a slatted pergola that lets light through but breaks the "
            "rain. I learned that outdoor fabric is worth every rupee, and that furniture should "
            "sit 10cm off the ground so water never pools under the legs. The lounge has now "
            "survived two full seasons and still looks new."
        ),
        "images": ["1616627561950-9f746e330187", "1600585154340-be6161a56a0c"],
    },
    {
        "title": "First woodworking workshop bench",
        "category": "workshop",
        "status": "pending",
        "description": (
            "After a woodworking basics course, my first real project was a proper workbench — "
            "hardwood top, mortise-and-tenon legs, and a twin-screw vice. It took three weekends "
            "and a lot of mistakes (measure twice, cut once is real). The bench is heavy, square "
            "and flat, and everything I build from now on will start on it. Attached is my course "
            "certificate and the plan I drew."
        ),
        "images": ["1538688525198-9b88f6f53126"],
    },
]


class Command(BaseCommand):
    help = "Seed the Aangan Living catalog (categories, brands, products, reviews)."

    def handle(self, *args, **options):
        self._seed_brands()
        self._seed_categories()
        self._seed_attributes()
        self._seed_products()
        self._seed_reviews()
        self._seed_community()
        self._seed_home()
        self.stdout.write(self.style.SUCCESS("Catalog seeded successfully."))

    def _seed_brands(self):
        for name, slug, country in BRANDS:
            Brand.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "country": country, "is_active": True},
            )

    def _seed_categories(self):
        for index, data in enumerate(CATEGORIES):
            parent, _ = Category.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "image_url": IMG.format(id=data["image"]),
                    "is_active": True,
                    "is_featured": True,
                    "sort_order": index,
                },
            )
            for child_index, (slug, name, image_id) in enumerate(data["children"]):
                Category.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "name": name,
                        "parent": parent,
                        "image_url": IMG.format(id=image_id),
                        "is_active": True,
                        "is_featured": False,
                        "sort_order": child_index,
                    },
                )

    def _seed_attributes(self):
        attributes = {
            "Color": ["Walnut", "Teak", "Oak", "Smoked", "Natural"],
            "Size": ["2-Seater", "3-Seater", "Queen", "King", "6-Seater"],
        }
        for name, values in attributes.items():
            attribute, _ = Attribute.objects.get_or_create(name=name)
            for value in values:
                AttributeValue.objects.get_or_create(attribute=attribute, value=value)
        self.color_attr = Attribute.objects.get(name="Color")

    def _seed_products(self):
        brands = {b.slug: b for b in Brand.objects.all()}
        categories = {c.slug: c for c in Category.objects.all()}
        random.seed(7)

        for (
            category_slug, name, slug, short, description, material,
            finish, dimensions, images, price, compare, stock, flags, brand_slug,
        ) in PRODUCTS:
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "brand": brands.get(brand_slug),
                    "category": categories[category_slug],
                    "short_description": short,
                    "description": description,
                    "material": material,
                    "finish": finish,
                    "dimensions": dimensions,
                    "assembly_required": random.choice([False, False, True]),
                    "warranty": "5-year frame warranty",
                    "is_active": True,
                    "is_featured": "featured" in flags,
                    "is_new": "new" in flags,
                    "is_bestseller": "bestseller" in flags,
                },
            )

            # variants — primary finish + optional second finish at +10%
            variant_names = [finish]
            if random.random() < 0.45:
                variant_names.append(
                    random.choice(["Walnut", "Teak", "Oak", "Smoked", "Natural"])
                )
            for i, vname in enumerate(dict.fromkeys(variant_names)):
                variant, _ = ProductVariant.objects.update_or_create(
                    sku=f"AAN-{slug[:6].upper()}-{i+1}",
                    defaults={
                        "product": product,
                        "name": vname,
                        "price": price + (price * 0.10 if i else 0),
                        "compare_price": compare,
                        "stock": max(0, stock - i * 2),
                        "is_active": True,
                    },
                )
                color_value = AttributeValue.objects.get_or_create(
                    attribute=self.color_attr, value=vname
                )[0]
                variant.attribute_values.set([color_value])

            # images
            ProductImage.objects.filter(product=product).delete()
            for i, image_id in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image_url=IMG.format(id=image_id),
                    alt_text=f"{name} — view {i+1}",
                    is_primary=i == 0,
                    sort_order=i,
                )

    def _seed_reviews(self):
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@aangan.pk",
                "first_name": "Demo",
                "last_name": "Customer",
                "is_staff": False,
            },
        )
        if not user.has_usable_password():
            user.set_password("demo1234")
            user.save()
        if not hasattr(user, "profile"):
            from accounts.models import Profile

            Profile.objects.create(user=user, phone="0300 1112223", city="Lahore")

        products = {p.slug: p for p in Product.objects.all()}
        for slug, rating, title, comment in DEMO_REVIEWS:
            product = products.get(slug)
            if not product:
                continue
            Review.objects.update_or_create(
                product=product,
                user=user,
                defaults={"rating": rating, "title": title, "comment": comment, "is_approved": True},
            )

    def _seed_community(self):
        from community.models import Project, ProjectImage

        user = get_user_model().objects.filter(username="demo").first()
        if not user:
            self.stdout.write(self.style.WARNING("Demo user not found; skipping community seed."))
            return

        seed_dir = settings.MEDIA_ROOT / "community" / "seed"
        seed_dir.mkdir(parents=True, exist_ok=True)

        for data in DEMO_PROJECTS:
            project, created = Project.objects.update_or_create(
                user=user,
                title=data["title"],
                defaults={
                    "category": data["category"],
                    "description": data["description"],
                    "status": data["status"],
                },
            )
            if not created:
                continue
            for i, image_id in enumerate(data["images"]):
                filename = f"{project.pk}-{image_id}.jpg"
                path = seed_dir / filename
                url = IMG.format(id=image_id)
                try:
                    with urllib.request.urlopen(url, timeout=20) as response:
                        path.write_bytes(response.read())
                except Exception as exc:
                    self.stdout.write(
                        self.style.WARNING(f"Community image download failed ({image_id}): {exc}")
                    )
                    continue
                ProjectImage.objects.create(
                    project=project,
                    image=f"community/seed/{filename}",
                    caption=f"{data['title']} — view {i+1}",
                    sort_order=i,
                )
        self.stdout.write(self.style.SUCCESS("Community projects seeded."))

    def _seed_home(self):
        from core.models import HeroSlide

        HERO_SLIDES = [
            {
                "heading": "Furniture that feels like home, built to last.",
                "subheading": "The Teak Edit — Autumn 2026",
                "cta_label": "Shop the collection",
                "cta_link": "/shop/",
                "image_id": "1555041469-a586c61ea9bc",
            },
            {
                "heading": "Gather around a table made for generations.",
                "subheading": "The dining room collection",
                "cta_label": "Explore dining",
                "cta_link": "/category/dining/",
                "image_id": "1615873968403-89e068629265",
            },
            {
                "heading": "Quiet luxury for the bedroom retreat.",
                "subheading": "New season — bedroom edit",
                "cta_label": "Shop bedroom",
                "cta_link": "/category/bedroom/",
                "image_id": "1616594039964-ae9021a400a0",
            },
        ]

        seed_dir = settings.MEDIA_ROOT / "hero" / "seed"
        seed_dir.mkdir(parents=True, exist_ok=True)

        for i, data in enumerate(HERO_SLIDES):
            slide, created = HeroSlide.objects.update_or_create(
                heading=data["heading"],
                defaults={
                    "subheading": data["subheading"],
                    "cta_label": data["cta_label"],
                    "cta_link": data["cta_link"],
                    "is_active": True,
                    "sort_order": i,
                },
            )
            if slide.desktop_image:
                continue
            filename = f"slide-{i}.jpg"
            path = seed_dir / filename
            url = IMG.format(id=data["image_id"])
            try:
                with urllib.request.urlopen(url, timeout=20) as response:
                    path.write_bytes(response.read())
                slide.desktop_image = f"hero/seed/{filename}"
                slide.save(update_fields=["desktop_image"])
            except Exception as exc:
                self.stdout.write(
                    self.style.WARNING(f"Hero image download failed ({data['image_id']}): {exc}")
                )

        spotlight = Product.objects.filter(is_active=True).first()
        if spotlight and not Product.objects.filter(is_spotlight=True).exists():
            spotlight.is_spotlight = True
            spotlight.save(update_fields=["is_spotlight"])

        self.stdout.write(self.style.SUCCESS("Home page content seeded."))
