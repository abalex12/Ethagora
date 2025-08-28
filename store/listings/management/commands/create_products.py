import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Category, SubCategory, Listing, ListingImage
import cloudinary.uploader

User = get_user_model()


class Command(BaseCommand):
    help = "Import listings from an Excel file and upload images from a folder"

    def add_arguments(self, parser):
        parser.add_argument('--excel', type=str, required=True, help="Absolute path to Excel file")
        parser.add_argument('--images', type=str, required=True, help="Absolute path to images folder")

    def handle(self, *args, **options):
        excel_path = options['excel']
        images_folder = options['images']

        if not os.path.exists(excel_path):
            self.stdout.write(self.style.ERROR(f"Excel file not found: {excel_path}"))
            return

        if not os.path.exists(images_folder):
            self.stdout.write(self.style.ERROR(f"Images folder not found: {images_folder}"))
            return

        df = pd.read_excel(excel_path)

        required_cols = ['title', 'description', 'price', 'category',
                         'subcategory', 'condition', 'location',
                         'contact_telegram', 'seller_email', 'images']
        for col in required_cols:
            if col not in df.columns:
                self.stdout.write(self.style.ERROR(f"Missing required column: {col}"))
                return

        for index, row in df.iterrows():
            try:
                # Find seller
                seller = User.objects.filter(email=row['seller_email']).first()
                if not seller:
                    self.stdout.write(self.style.WARNING(
                        f"Seller with email {row['seller_email']} not found (row {index+2}), skipping"
                    ))
                    continue

                # Find category
                try:
                    category = Category.objects.get(name=row['category'])
                except Category.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Category '{row['category']}' not found (row {index+2}), skipping"
                    ))
                    continue

                # Find subcategory
                subcategory = None
                if pd.notna(row['subcategory']):
                    try:
                        subcategory = SubCategory.objects.get(category=category, name=row['subcategory'])
                    except SubCategory.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f"SubCategory '{row['subcategory']}' not found in '{category.name}' (row {index+2}), skipping"
                        ))
                        continue

                # Create Listing
                listing = Listing.objects.create(
                    title=row['title'],
                    description=row['description'],
                    price=row['price'],
                    category=category,
                    subcategory=subcategory,
                    condition=row['condition'],
                    location=row['location'],
                    contact_telegram=row['contact_telegram'],
                    seller=seller,
                )

                # Handle images
                image_files = str(row['images']).split(",") if pd.notna(row['images']) else []
                for idx, image_file in enumerate(image_files):
                    image_file = image_file.strip()
                    image_path = os.path.join(images_folder, image_file)

                    if not os.path.exists(image_path):
                        self.stdout.write(self.style.WARNING(f"Image not found: {image_path}, skipping"))
                        continue

                    # Upload to Cloudinary
                    upload_result = cloudinary.uploader.upload(
                        image_path,
                        folder="listings"
                    )

                    # Save to ListingImage
                    ListingImage.objects.create(
                        listing=listing,
                        image=upload_result['public_id'],
                        is_primary=(idx == 0)
                    )

                self.stdout.write(self.style.SUCCESS(f"Imported listing: {listing.title}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error on row {index+2}: {str(e)}"))
