from django.core.management.base import BaseCommand
from listings.models import Category, SubCategory

class Command(BaseCommand):
    help = 'Create initial categories and subcategories with icons'

    def handle(self, *args, **options):
        categories_data = {
            'Electronics': {
                'icon': 'laptop',
                'subcategories': [
                    {'name': 'Mobile Phones', 'icon': 'mobile-alt'},
                    {'name': 'Laptops', 'icon': 'laptop'},
                    {'name': 'Tablets', 'icon': 'tablet-alt'},
                    {'name': 'Cameras', 'icon': 'camera'},
                    {'name': 'Audio & Headphones', 'icon': 'headphones'},
                    {'name': 'Gaming Consoles', 'icon': 'gamepad'},
                    {'name': 'Smart Home Devices', 'icon': 'home'},
                    {'name': 'Wearables', 'icon': 'watch'},
                    {'name': 'Drones', 'icon': 'drone'},
                    {'name': 'Accessories', 'icon': 'plug'}
                ]
            },
            'Vehicles': {
                'icon': 'car',
                'subcategories': [
                    {'name': 'Cars', 'icon': 'car'},
                    {'name': 'Motorcycles', 'icon': 'motorcycle'},
                    {'name': 'Bicycles', 'icon': 'bicycle'},
                    {'name': 'Trucks & Commercial', 'icon': 'truck'},
                    {'name': 'Auto Parts', 'icon': 'cog'},
                    {'name': 'Boats', 'icon': 'ship'},
                    {'name': 'RVs & Campers', 'icon': 'caravan'},
                    {'name': 'Electric Vehicles', 'icon': 'bolt'},
                    {'name': 'Scooters', 'icon': 'moped'},
                    {'name': 'Car Accessories', 'icon': 'tools'}
                ]
            },
            'Furniture': {
                'icon': 'couch',
                'subcategories': [
                    {'name': 'Living Room', 'icon': 'couch'},
                    {'name': 'Bedroom', 'icon': 'bed'},
                    {'name': 'Kitchen & Dining', 'icon': 'utensils'},
                    {'name': 'Office', 'icon': 'chair'},
                    {'name': 'Outdoor', 'icon': 'umbrella-beach'},
                    {'name': 'Antiques', 'icon': 'clock'},
                    {'name': 'Storage', 'icon': 'box'},
                    {'name': 'Kids Furniture', 'icon': 'baby-carriage'},
                    {'name': 'Mattresses', 'icon': 'bed'},
                    {'name': 'Home Decor', 'icon': 'paint-roller'}
                ]
            },
            'Fashion': {
                'icon': 'tshirt',
                'subcategories': [
                    {'name': 'Mens Clothing', 'icon': 'tshirt'},
                    {'name': 'Womens Clothing', 'icon': 'female'},
                    {'name': 'Shoes', 'icon': 'shoe-prints'},
                    {'name': 'Bags', 'icon': 'shopping-bag'},
                    {'name': 'Accessories', 'icon': 'glasses'},
                    {'name': 'Watches', 'icon': 'watch'},
                    {'name': 'Jewelry', 'icon': 'gem'},
                    {'name': 'Kids Clothing', 'icon': 'child'},
                    {'name': 'Athleisure', 'icon': 'running'},
                    {'name': 'Formal Wear', 'icon': 'user-tie'}
                ]
            },
            'Home & Garden': {
                'icon': 'home',
                'subcategories': [
                    {'name': 'Appliances', 'icon': 'blender'},
                    {'name': 'Kitchenware', 'icon': 'utensils'},
                    {'name': 'Garden Tools', 'icon': 'leaf'},
                    {'name': 'Decor', 'icon': 'paint-roller'},
                    {'name': 'Lighting', 'icon': 'lightbulb'},
                    {'name': 'Storage Solutions', 'icon': 'box'},
                    {'name': 'Bedding', 'icon': 'bed'},
                    {'name': 'Bathroom', 'icon': 'bath'},
                    {'name': 'Outdoor Living', 'icon': 'tree'},
                    {'name': 'Cleaning Supplies', 'icon': 'broom'}
                ]
            },
            'Sports & Recreation': {
                'icon': 'football-ball',
                'subcategories': [
                    {'name': 'Fitness Equipment', 'icon': 'dumbbell'},
                    {'name': 'Outdoor Sports', 'icon': 'hiking'},
                    {'name': 'Water Sports', 'icon': 'swimmer'},
                    {'name': 'Winter Sports', 'icon': 'skating'},
                    {'name': 'Team Sports', 'icon': 'basketball-ball'},
                    {'name': 'Camping Gear', 'icon': 'campground'},
                    {'name': 'Cycling', 'icon': 'bicycle'},
                    {'name': 'Fishing', 'icon': 'fish'},
                    {'name': 'Golf', 'icon': 'golf-ball'},
                    {'name': 'Athletic Apparel', 'icon': 'tshirt'}
                ]
            },
            'Books & Media': {
                'icon': 'book',
                'subcategories': [
                    {'name': 'Books', 'icon': 'book'},
                    {'name': 'Movies & TV', 'icon': 'film'},
                    {'name': 'Music', 'icon': 'music'},
                    {'name': 'Video Games', 'icon': 'gamepad'},
                    {'name': 'Magazines', 'icon': 'newspaper'},
                    {'name': 'Educational', 'icon': 'graduation-cap'},
                    {'name': 'Audiobooks', 'icon': 'headphones'},
                    {'name': 'Comics', 'icon': 'book-open'},
                    {'name': 'E-books', 'icon': 'tablet-alt'},
                    {'name': 'Vinyl Records', 'icon': 'record-vinyl'}
                ]
            },
            'Pets': {
                'icon': 'paw',
                'subcategories': [
                    {'name': 'Dogs', 'icon': 'dog'},
                    {'name': 'Cats', 'icon': 'cat'},
                    {'name': 'Fish & Aquarium', 'icon': 'fish'},
                    {'name': 'Birds', 'icon': 'dove'},
                    {'name': 'Small Pets', 'icon': 'otter'},
                    {'name': 'Pet Supplies', 'icon': 'bone'},
                    {'name': 'Reptiles', 'icon': 'dragon'},
                    {'name': 'Pet Grooming', 'icon': 'brush'},
                    {'name': 'Pet Training', 'icon': 'dog-leashed'},
                    {'name': 'Pet Accessories', 'icon': 'collar'}
                ]
            },
            'Services': {
                'icon': 'tools',
                'subcategories': [
                    {'name': 'Home Services', 'icon': 'tools'},
                    {'name': 'Automotive Services', 'icon': 'car-battery'},
                    {'name': 'Personal Services', 'icon': 'user'},
                    {'name': 'Professional Services', 'icon': 'briefcase'},
                    {'name': 'Educational Services', 'icon': 'chalkboard-teacher'},
                    {'name': 'Health & Beauty', 'icon': 'heart'},
                    {'name': 'Event Planning', 'icon': 'calendar-alt'},
                    {'name': 'Repair Services', 'icon': 'wrench'},
                    {'name': 'Cleaning Services', 'icon': 'broom'},
                    {'name': 'Financial Services', 'icon': 'dollar-sign'}
                ]
            },
            'Jobs': {
                'icon': 'briefcase',
                'subcategories': [
                    {'name': 'Full Time', 'icon': 'clock'},
                    {'name': 'Part Time', 'icon': 'hourglass-half'},
                    {'name': 'Contract', 'icon': 'file-contract'},
                    {'name': 'Internship', 'icon': 'user-graduate'},
                    {'name': 'Remote Work', 'icon': 'laptop-house'},
                    {'name': 'Freelance', 'icon': 'pen'},
                    {'name': 'Temporary', 'icon': 'hourglass'},
                    {'name': 'Seasonal', 'icon': 'leaf'},
                    {'name': 'Volunteer', 'icon': 'hands-helping'},
                    {'name': 'Executive', 'icon': 'user-tie'}
                ]
            },
            'Food & Beverages': {
                'icon': 'utensils',
                'subcategories': [
                    {'name': 'Fruits & Vegetables', 'icon': 'carrot'},
                    {'name': 'Meat & Seafood', 'icon': 'fish'},
                    {'name': 'Dairy', 'icon': 'cheese'},
                    {'name': 'Bakery', 'icon': 'bread-slice'},
                    {'name': 'Beverages', 'icon': 'coffee'},
                    {'name': 'Snacks', 'icon': 'cookie'},
                    {'name': 'Organic Foods', 'icon': 'leaf'},
                    {'name': 'Canned Goods', 'icon': 'can'},
                    {'name': 'Spices & Seasonings', 'icon': 'pepper-hot'},
                    {'name': 'Desserts', 'icon': 'ice-cream'}
                ]
            },
            'Travel': {
                'icon': 'plane',
                'subcategories': [
                    {'name': 'Flights', 'icon': 'plane'},
                    {'name': 'Hotels', 'icon': 'hotel'},
                    {'name': 'Car Rentals', 'icon': 'car'},
                    {'name': 'Cruises', 'icon': 'ship'},
                    {'name': 'Tours', 'icon': 'map'},
                    {'name': 'Camping', 'icon': 'campground'},
                    {'name': 'Adventure Travel', 'icon': 'hiking'},
                    {'name': 'Travel Accessories', 'icon': 'suitcase'},
                    {'name': 'Vacation Packages', 'icon': 'umbrella-beach'},
                    {'name': 'Travel Insurance', 'icon': 'shield-alt'}
                ]
            },
            'Health & Wellness': {
                'icon': 'heart',
                'subcategories': [
                    {'name': 'Vitamins & Supplements', 'icon': 'capsules'},
                    {'name': 'Fitness Equipment', 'icon': 'dumbbell'},
                    {'name': 'Personal Care', 'icon': 'brush'},
                    {'name': 'Medical Supplies', 'icon': 'first-aid'},
                    {'name': 'Skincare', 'icon': 'spa'},
                    {'name': 'Haircare', 'icon': 'scissors'},
                    {'name': 'Mental Health', 'icon': 'brain'},
                    {'name': 'Nutrition', 'icon': 'apple-alt'},
                    {'name': 'Alternative Medicine', 'icon': 'mortar-pestle'},
                    {'name': 'Wellness Services', 'icon': 'hand-holding-heart'}
                ]
            },
            'Toys & Games': {
                'icon': 'puzzle-piece',
                'subcategories': [
                    {'name': 'Action Figures', 'icon': 'robot'},
                    {'name': 'Board Games', 'icon': 'dice'},
                    {'name': 'Puzzles', 'icon': 'puzzle-piece'},
                    {'name': 'Dolls', 'icon': 'doll'},
                    {'name': 'Building Sets', 'icon': 'cubes'},
                    {'name': 'Educational Toys', 'icon': 'graduation-cap'},
                    {'name': 'Outdoor Toys', 'icon': 'football-ball'},
                    {'name': 'Electronic Toys', 'icon': 'battery-full'},
                    {'name': 'Collectibles', 'icon': 'star'},
                    {'name': 'Craft Kits', 'icon': 'paint-brush'}
                ]
            },
            'Art & Crafts': {
                'icon': 'paint-brush',
                'subcategories': [
                    {'name': 'Painting Supplies', 'icon': 'paint-brush'},
                    {'name': 'Drawing Tools', 'icon': 'pencil-alt'},
                    {'name': 'Sculpting', 'icon': 'hammer'},
                    {'name': 'Crafting Materials', 'icon': 'cut'},
                    {'name': 'Sewing & Knitting', 'icon': 'thread'},
                    {'name': 'Scrapbooking', 'icon': 'book'},
                    {'name': 'Jewelry Making', 'icon': 'gem'},
                    {'name': 'Pottery', 'icon': 'mug-saucer'},
                    {'name': 'Printmaking', 'icon': 'print'},
                    {'name': 'DIY Kits', 'icon': 'tools'}
                ]
            }
        }

        for category_name, data in categories_data.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={
                    'slug': category_name.lower().replace(' ', '-').replace('&', 'and'),
                    'icon': data['icon']
                }
            )
            
            if created:
                self.stdout.write(f"Created category: {category_name}")
            
            for subcategory_data in data['subcategories']:
                subcategory, sub_created = SubCategory.objects.get_or_create(
                    category=category,
                    name=subcategory_data['name'],
                    defaults={
                        'slug': subcategory_data['name'].lower().replace(' ', '-').replace('&', 'and'),
                        'icon': subcategory_data['icon']
                    }
                )
                
                if sub_created:
                    self.stdout.write(f"  Created subcategory: {subcategory_data['name']}")

        self.stdout.write(self.style.SUCCESS('Successfully created categories and subcategories'))