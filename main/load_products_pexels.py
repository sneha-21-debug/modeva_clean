import os
import sys
import django
import requests
import random
from io import BytesIO
from django.core.files import File

# ✅ Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modeva.settings')
django.setup()

# ✅ Import your model
from main.models import Product

# ✅ Pexels API setup
PEXELS_API_KEY = "2U9pyswNEs0sH1z2omzbARaeLSRVgHLnbYilzTNYz1vIL5q6V5WNP1JH"
PEXELS_API_URL = "https://api.pexels.com/v1/search"

# ✅ Category and subcategories
categories = {
    "men": ["men shirts", "men jeans", "men jackets", "men shoes"],
    "women": ["women dresses", "women tops", "women jeans", "women sarees"],
    "kids": ["kids tshirts", "kids pants", "kids shoes", "kids toys"],
    "accessories": ["handbags", "sunglasses", "watches", "jewellery"]
}

# ✅ Media folder setup
media_folder = os.path.join(os.getcwd(), "media", "product_images")
os.makedirs(media_folder, exist_ok=True)

print("🚀 Starting bulk product import using Pexels API...\n")

headers = {"Authorization": PEXELS_API_KEY}

total_added = 0

for category, subcategories in categories.items():
    print(f"📦 Adding products for category: {category}")
    for subcat in subcategories:
        for i in range(20):  # 20 products per subcategory
            try:
                # Get image from Pexels API
                response = requests.get(
                    PEXELS_API_URL,
                    headers=headers,
                    params={"query": subcat, "per_page": 1, "page": random.randint(1, 50)},
                    timeout=10
                )

                if response.status_code == 200 and response.json().get("photos"):
                    image_url = response.json()["photos"][0]["src"]["large"]
                    image_data = requests.get(image_url).content

                    # Create product instance
                    product = Product(
                        name=f"{subcat.title()} {i+1}",
                        category=category,
                        subcategory=subcat.replace(" ", "_"),
                        price=round(random.uniform(499, 4999), 2),
                        description=f"Trendy {subcat} now available on Modeva!",
                        stock=random.randint(10, 100),
                        featured=random.choice([True, False])
                    )

                    # Save image file
                    image_name = f"{subcat}_{i+1}.jpg"
                    image_path = os.path.join(media_folder, image_name)
                    with open(image_path, "wb") as f:
                        f.write(image_data)

                    product.image.save(image_name, File(open(image_path, "rb")))
                    product.save()
                    total_added += 1
                    print(f"   ✅ Added: {subcat.title()} {i+1}")
                else:
                    print(f"   ⚠️ Failed to fetch image for {subcat} (status {response.status_code})")

            except Exception as e:
                print(f"   ⚠️ Error adding {subcat} {i+1}: {e}")

print(f"\n🎉 Done! Successfully added {total_added} products with images!\n")
