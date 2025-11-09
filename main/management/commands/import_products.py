import csv, os
from django.core.files import File
from django.core.management.base import BaseCommand
from main.models import Product

class Command(BaseCommand):
    help = "Import products from CSV. Columns: name, category, price, description, image_path, stock, featured"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **opts):
        csv_path = opts['csv_path']
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prod = Product(
                    name=row['name'],
                    category=row['category'],
                    price=row['price'],
                    description=row.get('description', ''),
                    stock=int(row.get('stock', 10)),
                    featured=(row.get('featured', '').lower() == 'true'),
                )
                img_path = row.get('image_path', '').strip()
                if img_path and os.path.exists(img_path):
                    with open(img_path, 'rb') as imgf:
                        prod.image.save(os.path.basename(img_path), File(imgf), save=False)
                prod.save()
        self.stdout.write(self.style.SUCCESS('✅ Products imported successfully!'))
