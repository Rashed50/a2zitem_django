import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

##? Models Import
from apps.product.models.category import Category

"""
##TODO:- python manage.py BulkCategory
"""
class Command(BaseCommand):
    help = 'Bulk category creation from predefined data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk category creation...'))
        
        categories = [
            ##! ============================================
            ##!              Main Categories
            ##! ============================================
            {
                "name": "Electronics",
                "parent": None
            },
            {
                "name": "Fashion",
                "parent": None
            },
            {
                "name": "Home & Living",
                "parent": None
            },
            {
                "name": "Books & Education",
                "parent": None
            },
            {
                "name": "Sports",
                "parent": None
            },
            
            ##! ============================================
            ##!              Sub Categories
            ##! ============================================
            
            ##? Electronics Subcategories
            {
                "name": "Mobile Phones",
                "parent": "Electronics"
            },
            {
                "name": "Computers",
                "parent": "Electronics"
            },
            {
                "name": "Gadgets",
                "parent": "Electronics"
            },
            
            ##? Mobile Phone Subcategories
            {
                "name": "Smartphones",
                "parent": "Mobile Phones"
            },
            {
                "name": "Feature Phones",
                "parent": "Mobile Phones"
            },
            
            ##? Computers Subcategories
            {
                "name": "Desktops",
                "parent": "Computers"
            },
            {
                "name": "Laptops",
                "parent": "Computers"
            },
            {
                "name": "Tablets",
                "parent": "Computers"
            },
            
            ##? Gadgets Subcategories
            {
                "name": "Smart Watches",
                "parent": "Gadgets"
            },
            {
                "name": "Headphones",
                "parent": "Gadgets"
            },
            {
                "name": "Power Banks",
                "parent": "Gadgets"
            },
            
            ##? Fashion Subcategories
            {
                "name": "Men's Fashion",
                "parent": "Fashion"
            },
            {
                "name": "Women's Fashion",
                "parent": "Fashion"
            },
            {
                "name": "Kids' Fashion",
                "parent": "Fashion"
            },
            
            ##? Men's Fashion Subcategories
            {
                "name": "Shirts",
                "parent": "Men's Fashion"
            },
            {
                "name": "Pants",
                "parent": "Men's Fashion"
            },
            {
                "name": "Shoes",
                "parent": "Men's Fashion"
            },
            
            ##? Women's Fashion Subcategories
            {
                "name": "Saris",
                "parent": "Women's Fashion"
            },
            {
                "name": "Three-piece",
                "parent": "Women's Fashion"
            },
            {
                "name": "Women's Shoes",
                "parent": "Women's Fashion"
            },
            
            ##? Kids' Fashion Subcategories
            {
                "name": "Baby Dresses",
                "parent": "Kids' Fashion"
            },
            {
                "name": "School Uniforms",
                "parent": "Kids' Fashion"
            },
            
            ##? Home & Living Subcategories
            {
                "name": "Furniture",
                "parent": "Home & Living"
            },
            {
                "name": "Kitchen",
                "parent": "Home & Living"
            },
            {
                "name": "Decor",
                "parent": "Home & Living"
            },
            
            ##? Furniture Subcategories
            {
                "name": "Sofas",
                "parent": "Furniture"
            },
            {
                "name": "Dining Tables",
                "parent": "Furniture"
            },
            {
                "name": "Beds",
                "parent": "Furniture"
            },
            
            ##? Kitchen Subcategories
            {
                "name": "Cookware",
                "parent": "Kitchen"
            },
            {
                "name": "Dinner Sets",
                "parent": "Kitchen"
            },
            
            ##? Decor Subcategories
            {
                "name": "Wall Art",
                "parent": "Decor"
            },
            {
                "name": "Vases",
                "parent": "Decor"
            },
            
            ##? Books & Education Subcategories
            {
                "name": "Academic Books",
                "parent": "Books & Education"
            },
            {
                "name": "Story Books",
                "parent": "Books & Education"
            },
            
            ##? Academic Books Subcategories
            {
                "name": "Science Books",
                "parent": "Academic Books"
            },
            {
                "name": "Math Books",
                "parent": "Academic Books"
            },
            {
                "name": "English Books",
                "parent": "Academic Books"
            },
            
            ##? Story Books Subcategories
            {
                "name": "Novels",
                "parent": "Story Books"
            },
            {
                "name": "Short Stories",
                "parent": "Story Books"
            },
            {
                "name": "Comics",
                "parent": "Story Books"
            },
            
            ##? Sports Subcategories
            {
                "name": "Cricket",
                "parent": "Sports"
            },
            {
                "name": "Football",
                "parent": "Sports"
            },
            {
                "name": "Badminton",
                "parent": "Sports"
            },
            
            ##? Cricket Subcategories
            {
                "name": "Cricket Bats",
                "parent": "Cricket"
            },
            {
                "name": "Cricket Balls",
                "parent": "Cricket"
            },
            {
                "name": "Cricket Pads",
                "parent": "Cricket"
            },
            
            ##? Football Subcategories
            {
                "name": "Football Balls",
                "parent": "Football"
            },
            {
                "name": "Football Jerseys",
                "parent": "Football"
            },
            {
                "name": "Football Boots",
                "parent": "Football"
            },
            
            ##? Badminton Subcategories
            {
                "name": "Badminton Rackets",
                "parent": "Badminton"
            },
            {
                "name": "Shuttlecocks",
                "parent": "Badminton"
            }
        ]
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        # First, create all parent categories
        parent_categories = {}
        
        for category_data in categories:
            try:
                parent_name = category_data.get("parent")
                
                # Get parent instance if exists
                parent_instance = None
                if parent_name:
                    try:
                        parent_instance = Category.objects.get(name=parent_name)
                    except Category.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Parent "{parent_name}" not found yet, will create later'))
                        # Store for later processing
                        parent_categories[category_data["name"]] = {
                            "data": category_data,
                            "parent_name": parent_name
                        }
                        continue
                
                # Create or update category
                obj, created = Category.objects.update_or_create(
                    name=category_data["name"],
                    defaults={
                        "parent": parent_instance
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Created: {category_data["name"]}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'🔄 Updated: {category_data["name"]}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {category_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        # Process categories that were skipped due to missing parents
        retry_count = 0
        for cat_name, cat_info in parent_categories.items():
            try:
                if cat_info["parent_name"]:
                    try:
                        parent_instance = Category.objects.get(name=cat_info["parent_name"])
                        
                        obj, created = Category.objects.update_or_create(
                            name=cat_info["data"]["name"],
                            defaults={
                                "parent": parent_instance
                            }
                        )
                        
                        if created:
                            created_count += 1
                            retry_count += 1
                            self.stdout.write(self.style.SUCCESS(f'✅ Created (retry): {cat_info["data"]["name"]}'))
                        else:
                            updated_count += 1
                            retry_count += 1
                            self.stdout.write(self.style.WARNING(f'🔄 Updated (retry): {cat_info["data"]["name"]}'))
                    except Category.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'❌ Parent "{cat_info["parent_name"]}" still not found for {cat_name}'))
                        skipped_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error in retry for {cat_name}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk category creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   └─ Total: {created_count + updated_count + skipped_count}\n'
        ))