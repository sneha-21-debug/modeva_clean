import os
import django
import requests
import random
from io import BytesIO
from django.core.files import File

# --- SETUP DJANGO ENVIRONMENT ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modeva.settings")
django.setup()

from main.models import Product

# --- PEXELS API CONFIGURATION ---
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"  # <-- Paste your key here
PEXELS_URL = "https://api.pexels.com/v1/search"

headers = {"Authorization": PEXELS_API_KEY}

# --- CATEGORY & SUBCATEGORY MAPPING ---
categories = {
    "accessories": ["handbags", "sunglasses", "watches", "jewellery"],
    "men": ["men_shirts", "men_jeans", "men_jackets", "men_shoes"],
    "women": ["women_dresses", "women_tops", "women_jeans", "women_sarees"],
    "kids": ["kids_tshirts", "kids_pants", "kids_shoes", "kids_toys"],
}

# --- CREATE MEDIA FOLDER ---
media_folder = os.path.join("media", "product_images")
os.makedirs(media_folder, exist_ok=True)

# --- ADD PRODUCTS AUTOMATICALLY ---
print("🚀 Starting automatic product import...\n")

total_added = 0

for category, subcategories in categories.items():
    print(f"📦 Adding products for category: {category}")
    for subcat in subcategories:
        query = subcat.replace("_", " ")
        params = {"query": query, "per_page": 20}
        response = requests.get(PEXELS_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"   ⚠️ Failed to fetch images for {query} ({response.status_code})")
            continue

        data = response.json().get("photos", [])
        print(f"   ➕ Adding {len(data)} products for {query}...")

        for i, photo in enumerate(data):
            image_url = photo["src"]["medium"]
            image_data = requests.get(image_url)

            if image_data.status_code == 200:
                image_name = f"{subcat}_{i+1}.jpg"
                image_path = os.path.join(media_folder, image_name)
                with open(image_path, "wb") as f:
                    f.write(image_data.content)

                product = Product(
                    name=f"{query.title()} {i+1}",
                    category=category,
                    subcategory=subcat,
                    price=round(random.uniform(499, 4999), 2),
                    description=f"Beautiful {query} from Modeva’s {category} collection ✨",
                    stock=random.randint(5, 50),
                    featured=random.choice([True, False]),
                )

                with open(image_path, "rb") as img_file:
                    product.image.save(image_name, File(img_file), save=True)

                total_added += 1

print(f"\n✅ Successfully added {total_added} products to the database!")
