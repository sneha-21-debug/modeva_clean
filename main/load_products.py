import os
import django
import random

# --- Setup Django environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modeva.settings')
django.setup()

from main.models import Product

# --- Define categories and subcategories ---
categories = {
    'men': ['men_shirts', 'men_jeans', 'men_jackets', 'men_shoes'],
    'women': ['women_dresses', 'women_tops', 'women_jeans', 'women_sarees'],
    'kids': ['kids_tshirts', 'kids_pants', 'kids_shoes', 'kids_toys'],
    'accessories': ['handbags', 'sunglasses', 'watches', 'jewellery']
}

# --- Folder where your images are stored ---
MEDIA_PATH = os.path.join('media', 'product_images')

# --- Ensure folder exists ---
if not os.path.exists(MEDIA_PATH):
    print(f"⚠️ Folder not found: {MEDIA_PATH}")
    print("Please create 'media/product_images' and add product images there.")
    exit()

# --- Some word lists for random names ---
adjectives = [
    "Trendy", "Stylish", "Elegant", "Classic", "Luxury", "Casual", "Modern", "Cool",
    "Comfy", "Bold", "Vibrant", "Smart", "Sleek", "Premium", "Chic"
]

product_types = {
    'men_shirts': ["Formal Shirt", "Casual Shirt", "Check Shirt", "Printed Shirt"],
    'men_jeans': ["Slim Jeans", "Ripped Jeans", "Denim Pants", "Stretch Jeans"],
    'men_jackets': ["Leather Jacket", "Hoodie", "Denim Jacket", "Bomber Jacket"],
    'men_shoes': ["Sneakers", "Formal Shoes", "Boots", "Loafers"],

    'women_dresses': ["Floral Dress", "Bodycon Dress", "Evening Gown", "Midi Dress"],
    'women_tops': ["Crop Top", "Blouse", "Tank Top", "T-Shirt"],
    'women_jeans': ["High Waist Jeans", "Skinny Jeans", "Mom Jeans", "Wide Leg Jeans"],
    'women_sarees': ["Silk Saree", "Cotton Saree", "Georgette Saree", "Chiffon Saree"],

    'kids_tshirts': ["Printed Tee", "Cartoon Tee", "Striped Tee", "Solid Tee"],
    'kids_pants': ["Denim Pants", "Joggers", "Shorts", "Cargo Pants"],
    'kids_shoes': ["Sneakers", "Sandals", "Boots", "Slip-ons"],
    'kids_toys': ["Soft Toy", "Car Toy", "Building Blocks", "Puzzle Toy"],

    'handbags': ["Leather Bag", "Tote Bag", "Clutch", "Sling Bag"],
    'sunglasses': ["Aviator", "Round", "Cat Eye", "Wayfarer"],
    'watches': ["Analog Watch", "Digital Watch", "Smart Watch", "Chronograph"],
    'jewellery': ["Earrings", "Necklace", "Bracelet", "Ring"],
}

# --- Delete old products before adding new ---
Product.objects.all().delete()
print("🧹 Cleared old product data.")

count = 0

for category, subcats in categories.items():
    for subcat in subcats:
        for i in range(1, 21):  # 20 products per subcategory
            adjective = random.choice(adjectives)
            item_name = random.choice(product_types[subcat])
            product_name = f"{adjective} {item_name} {i}"

            price = round(random.uniform(499, 4999), 2)
            stock = random.randint(5, 100)

            # Pick random image name (make sure you have images like 1.jpg ... 20.jpg)
            image_name = f"{random.randint(1,20)}.jpg"
            image_path = os.path.join(MEDIA_PATH, image_name)

            Product.objects.create(
                name=product_name,
                category=category,
                subcategory=subcat,
                price=price,
                description=f"Discover our {product_name} – perfect addition to your {category} collection!",
                image=f"product_images/{image_name}" if os.path.exists(image_path) else None,
                stock=stock,
                featured=random.choice([True, False])
            )

            count += 1

print(f"✅ Successfully added {count} products (20 per subcategory)!")
