import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

##? Models Import
from apps.product.models.brand import Brand

"""
##TODO:- python manage.py BulkBrand
"""
class Command(BaseCommand):
    help = 'Bulk brand creation from predefined data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk brand creation...'))
        
        brands = [
            ##! Electronics Brands
            {"name": "Apple"},
            {"name": "Samsung"},
            {"name": "Xiaomi"},
            {"name": "OnePlus"},
            {"name": "Google"},
            {"name": "Sony"},
            {"name": "LG"},
            {"name": "Panasonic"},
            {"name": "Philips"},
            {"name": "Lenovo"},
            {"name": "HP"},
            {"name": "Dell"},
            {"name": "Asus"},
            {"name": "Acer"},
            {"name": "Microsoft"},
            {"name": "Nokia"},
            {"name": "Motorola"},
            {"name": "Realme"},
            {"name": "Oppo"},
            {"name": "Vivo"},
            {"name": "Huawei"},
            {"name": "Honor"},
            {"name": "Toshiba"},
            {"name": "Canon"},
            {"name": "Nikon"},
            {"name": "GoPro"},
            {"name": "Bose"},
            {"name": "JBL"},
            {"name": "Sennheiser"},
            {"name": "Logitech"},
            
            ##! Home Appliances Brands
            {"name": "Whirlpool"},
            {"name": "LG"},
            {"name": "Samsung"},
            {"name": "General Electric"},
            {"name": "Bosch"},
            {"name": "Siemens"},
            {"name": "Miele"},
            {"name": "Electrolux"},
            {"name": "Haier"},
            {"name": "Sharp"},
            {"name": "Daikin"},
            {"name": "Gree"},
            {"name": "Voltas"},
            
            ##! Fashion Brands
            {"name": "Nike"},
            {"name": "Adidas"},
            {"name": "Puma"},
            {"name": "Reebok"},
            {"name": "Under Armour"},
            {"name": "Levi's"},
            {"name": "Zara"},
            {"name": "H&M"},
            {"name": "Uniqlo"},
            {"name": "Gucci"},
            {"name": "Prada"},
            {"name": "Louis Vuitton"},
            {"name": "Chanel"},
            {"name": "Dior"},
            {"name": "Versace"},
            {"name": "Armani"},
            {"name": "Ralph Lauren"},
            {"name": "Tommy Hilfiger"},
            {"name": "Calvin Klein"},
            {"name": "Hugo Boss"},
            {"name": "Lacoste"},
            {"name": "Ray-Ban"},
            {"name": "Oakley"},
            {"name": "Fossil"},
            {"name": "Casio"},
            {"name": "Seiko"},
            {"name": "Titan"},
            {"name": "Rolex"},
            {"name": "Omega"},
            {"name": "Tag Heuer"},
            
            ##! Sports Brands
            {"name": "Nike"},
            {"name": "Adidas"},
            {"name": "Puma"},
            {"name": "Reebok"},
            {"name": "Under Armour"},
            {"name": "New Balance"},
            {"name": "Asics"},
            {"name": "Fila"},
            {"name": "Skechers"},
            {"name": "Wilson"},
            {"name": "Yonex"},
            {"name": "Head"},
            {"name": "Speedo"},
            {"name": "Arena"},
            
            ##! Beauty & Personal Care Brands
            {"name": "L'Oreal"},
            {"name": "Maybelline"},
            {"name": "Nivea"},
            {"name": "Dove"},
            {"name": "Garnier"},
            {"name": "Olay"},
            {"name": "Pond's"},
            {"name": "Lakme"},
            {"name": "MAC"},
            {"name": "Estée Lauder"},
            {"name": "Clinique"},
            {"name": "Lancôme"},
            {"name": "Shiseido"},
            {"name": "The Body Shop"},
            {"name": "Bath & Body Works"},
            {"name": "Victoria's Secret"},
            {"name": "Gillette"},
            {"name": "Philips"},
            {"name": "Braun"},
            
            ##! Automotive Brands
            {"name": "Toyota"},
            {"name": "Honda"},
            {"name": "Ford"},
            {"name": "Chevrolet"},
            {"name": "BMW"},
            {"name": "Mercedes-Benz"},
            {"name": "Audi"},
            {"name": "Volkswagen"},
            {"name": "Hyundai"},
            {"name": "Kia"},
            {"name": "Nissan"},
            {"name": "Mazda"},
            {"name": "Suzuki"},
            {"name": "Tesla"},
            {"name": "Ferrari"},
            {"name": "Lamborghini"},
            {"name": "Porsche"},
            {"name": "Jaguar"},
            {"name": "Land Rover"},
            {"name": "Volvo"},
            
            ##! Food & Beverage Brands
            {"name": "Coca-Cola"},
            {"name": "Pepsi"},
            {"name": "Nestlé"},
            {"name": "Cadbury"},
            {"name": "Mars"},
            {"name": "Kellogg's"},
            {"name": "Lipton"},
            {"name": "Nescafé"},
            {"name": "Starbucks"},
            {"name": "McDonald's"},
            {"name": "KFC"},
            {"name": "Pizza Hut"},
            {"name": "Domino's"},
            {"name": "Burger King"},
            {"name": "Subway"},
            
            ##! Furniture Brands
            {"name": "IKEA"},
            {"name": "Ashley Furniture"},
            {"name": "Herman Miller"},
            {"name": "Steelcase"},
            {"name": "La-Z-Boy"},
            {"name": "Restoration Hardware"},
            {"name": "Williams-Sonoma"},
            {"name": "Pottery Barn"},
            {"name": "Crate & Barrel"},
            {"name": "West Elm"},
            
            ##! Pet Brands
            {"name": "Pedigree"},
            {"name": "Whiskas"},
            {"name": "Royal Canin"},
            {"name": "Hill's Science Diet"},
            {"name": "Purina"},
            {"name": "Iams"},
            {"name": "Eukanuba"},
            
            ##! Toy Brands
            {"name": "LEGO"},
            {"name": "Mattel"},
            {"name": "Hasbro"},
            {"name": "Fisher-Price"},
            {"name": "Hot Wheels"},
            {"name": "Barbie"},
            {"name": "Nerf"},
            {"name": "Play-Doh"},
            {"name": "Disney"},
            {"name": "Marvel"},
            {"name": "DC Comics"},
            
            ##! Book Publishers
            {"name": "Penguin Random House"},
            {"name": "HarperCollins"},
            {"name": "Simon & Schuster"},
            {"name": "Hachette Book Group"},
            {"name": "Macmillan Publishers"},
            {"name": "Oxford University Press"},
            {"name": "Cambridge University Press"},
            {"name": "Pearson"},
            {"name": "McGraw-Hill"},
            {"name": "Wiley"},
            
            ##! Bangladeshi Brands
            {"name": "Pran"},
            {"name": "Square"},
            {"name": "Beximco"},
            {"name": "ACI"},
            {"name": "Akij"},
            {"name": "RFL"},
            {"name": "Partex"},
            {"name": "Aarong"},
            {"name": "Yellow"},
            {"name": "Ecstasy"},
            {"name": "Sailor"},
            {"name": "Bata"},
            {"name": "Apex"},
            {"name": "Lotto"},
            {"name": "Martinez"},
            {"name": "Le Reve"},
            {"name": "Anjan's"},
            {"name": "Zaber & Zubair"},
            {"name": "Chorki"},
            {"name": "Pathao"},
            {"name": "Shohoz"},
            {"name": "Foodpanda"},
            {"name": "HungryNaki"},
            {"name": "Daraz"},
            {"name": "Pickaboo"},
            {"name": "Priyoshop"},
            {"name": "Evaly"},
            {"name": "Bkash"},
            {"name": "Nagad"},
            {"name": "Rocket"}
        ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_brands = []
        for brand in brands:
            if brand["name"] not in seen:
                seen.add(brand["name"])
                unique_brands.append(brand)
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for brand_data in unique_brands:
            try:
                # Create or update brand
                obj, created = Brand.objects.update_or_create(
                    name=brand_data["name"],
                    defaults={}  # No additional fields to update
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Created: {brand_data["name"]}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'🔄 Updated: {brand_data["name"]}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {brand_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk brand creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   └─ Total Brands: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Brands: {len(unique_brands)} (after removing duplicates)\n'
        ))