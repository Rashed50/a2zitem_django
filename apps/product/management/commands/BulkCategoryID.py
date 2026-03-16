import json
import os
import random
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from mptt.utils import tree_item_iterator

##? Models Import
from apps.product.models.category import Category
from .data.categoriesDataSheet import categories_data

"""
##TODO:- python manage.py BulkCategoryID
"""
class Command(BaseCommand):
    help = 'Bulk category creation from predefined data'
    
    def generate_random_id(self, min_id=1001, max_id=9999):
        """Generate random ID between min_id and max_id"""
        return random.randint(min_id, max_id)
    
    def get_unique_id(self, preferred_id=None, min_id=1001, max_id=9999):
        """
        Get a unique ID for category.
        If preferred_id is provided and not taken, use it.
        Otherwise generate random unique ID.
        """
        if preferred_id:
            # Check if preferred_id is available
            if not Category.objects.filter(id=preferred_id).exists():
                return preferred_id
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Preferred ID {preferred_id} is taken, generating random ID'))
        
        # Generate random unique ID
        while True:
            random_id = self.generate_random_id(min_id, max_id)
            if not Category.objects.filter(id=random_id).exists():
                return random_id
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk category creation with custom IDs...'))
        
        categories = categories_data
        
        # Remove duplicates while preserving order
        seen_names = set()
        seen_ids = set()
        unique_categories = []
        
        for category in categories:
            if category["name"] not in seen_names:
                # Check for duplicate preferred IDs
                if category["preferred_id"] in seen_ids:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ Duplicate preferred ID {category["preferred_id"]} for {category["name"]}, will generate random ID'
                    ))
                    category["preferred_id"] = None  # Will generate random
                
                seen_names.add(category["name"])
                if category["preferred_id"]:
                    seen_ids.add(category["preferred_id"])
                unique_categories.append(category)
        
        self.stdout.write(self.style.WARNING(f'Total categories to process: {len(unique_categories)}'))
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        id_conflicts = 0
        
        # First pass: Create all categories with parent=None
        category_objects = {}
        
        # Sort categories: parents first, then children
        # First create all main categories (parent=None)
        main_categories = [c for c in unique_categories if c["parent"] is None]
        other_categories = [c for c in unique_categories if c["parent"] is not None]
        
        # Process in order: main categories first, then others
        sorted_categories = main_categories + other_categories
        
        with transaction.atomic():
            for category_data in sorted_categories:
                try:
                    # Get unique ID (preferred or random)
                    final_id = self.get_unique_id(category_data.get("preferred_id"))
                    
                    if category_data.get("preferred_id") and category_data["preferred_id"] != final_id:
                        id_conflicts += 1
                    
                    # Create category without parent first
                    try:
                        category = Category(id=final_id, name=category_data["name"])
                        category.save()
                        category_objects[category_data["name"]] = category
                        created_count += 1
                        
                    except IntegrityError:
                        # If ID exists, create with new ID
                        new_id = self.get_unique_id(min_id=1001, max_id=9999)
                        category = Category(id=new_id, name=category_data["name"])
                        category.save()
                        category_objects[category_data["name"]] = category
                        created_count += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error creating {category_data["name"]}: {str(e)}'))
                    skipped_count += 1
        
        # Second pass: Update parent relationships in correct order
        parent_update_count = 0
        
        for category_data in sorted_categories:
            try:
                if category_data["parent"]:
                    category = category_objects.get(category_data["name"])
                    parent_name = category_data["parent"]
                    parent = category_objects.get(parent_name)
                    
                    if category and parent:
                        # Debug info
                        self.stdout.write(self.style.WARNING(
                            f'🔍 Processing: {category.name} -> {parent.name}'
                        ))
                        
                        # Check if trying to set self as parent
                        if parent.pk == category.pk:
                            self.stdout.write(self.style.ERROR(f'❌ Cannot set self as parent for {category.name}'))
                            continue
                        
                        # For MPTT, we need to check if parent is a descendant
                        # But since we just created all nodes, we need to refresh from DB
                        category.refresh_from_db()
                        parent.refresh_from_db()
                        
                        # Check if parent is actually a descendant
                        if parent.is_descendant_of(category):
                            self.stdout.write(self.style.ERROR(
                                f'❌ Cannot set descendant "{parent.name}" as parent of "{category.name}"'
                            ))
                            continue
                        
                        # Set parent
                        category.parent = parent
                        category.save()
                        parent_update_count += 1
                        self.stdout.write(self.style.SUCCESS(f'✅ Linked: {category.name} -> {parent.name}'))
                    elif category and not parent:
                        self.stdout.write(self.style.WARNING(f'⚠️ Parent "{parent_name}" not found for {category.name}'))
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error updating parent for {category_data["name"]}: {str(e)}'))
                import traceback
                self.stdout.write(self.style.ERROR(traceback.format_exc()))
        
        # Rebuild MPTT tree to ensure correct ordering
        self.stdout.write(self.style.WARNING('🔄 Rebuilding MPTT tree...'))
        Category.objects.rebuild()
        self.stdout.write(self.style.SUCCESS('✅ MPTT tree rebuilt successfully'))
        
        # Category wise count
        main_categories_count = len([c for c in unique_categories if c["parent"] is None])
        electronics = len([c for c in unique_categories if c["parent"] in ["Electronics", "Mobile Phones", "Computers", "Gadgets"] or 
                          (c["name"] in ["Mobile Phones", "Computers", "Gadgets", "Smartphones", "Feature Phones", 
                                        "Desktops", "Laptops", "Tablets", "Smart Watches", "Headphones", "Power Banks"])])
        
        fashion = len([c for c in unique_categories if c["parent"] in ["Fashion", "Men's Fashion", "Women's Fashion", "Kids' Fashion"] or
                      (c["name"] in ["Men's Fashion", "Women's Fashion", "Kids' Fashion", "Shirts", "Pants", "Shoes",
                                    "Saris", "Three-piece", "Women's Shoes", "Baby Dresses", "School Uniforms"])])
        
        home_living = len([c for c in unique_categories if c["parent"] in ["Home & Living", "Furniture", "Kitchen", "Decor"] or
                          (c["name"] in ["Furniture", "Kitchen", "Decor", "Sofas", "Dining Tables", "Beds",
                                        "Cookware", "Dinner Sets", "Wall Art", "Vases"])])
        
        books_education = len([c for c in unique_categories if c["parent"] in ["Books & Education", "Academic Books", "Story Books"] or
                              (c["name"] in ["Academic Books", "Story Books", "Science Books", "Math Books",
                                            "English Books", "Novels", "Short Stories", "Comics"])])
        
        sports = len([c for c in unique_categories if c["parent"] in ["Sports", "Cricket", "Football", "Badminton"] or
                     (c["name"] in ["Cricket", "Football", "Badminton", "Cricket Bats", "Cricket Balls", "Cricket Pads",
                                   "Football Balls", "Football Jerseys", "Football Boots", "Badminton Rackets", "Shuttlecocks"])])
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk category creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   ├─ Parent Links: {parent_update_count}\n'
            f'   ├─ ID Conflicts Resolved: {id_conflicts}\n'
            f'   └─ Total Categories: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Categories: {len(unique_categories)}\n'
            
            f'\n📋 Category Structure:\n'
            f'   ├─ Main Categories: {main_categories_count}\n'
            f'   │   ├─ Electronics: 1\n'
            f'   │   ├─ Fashion: 1\n'
            f'   │   ├─ Home & Living: 1\n'
            f'   │   ├─ Books & Education: 1\n'
            f'   │   └─ Sports: 1\n'
            f'   │\n'
            f'   ├─ Electronics Subcategories: {electronics}\n'
            f'   │   ├─ Level 1 (Mobile/Computers/Gadgets): 3\n'
            f'   │   └─ Level 2 (Smartphones/Desktops/Headphones etc): {electronics - 3}\n'
            f'   │\n'
            f'   ├─ Fashion Subcategories: {fashion}\n'
            f'   │   ├─ Level 1 (Men/Women/Kids): 3\n'
            f'   │   └─ Level 2 (Shirts/Saris/Shoes etc): {fashion - 3}\n'
            f'   │\n'
            f'   ├─ Home & Living Subcategories: {home_living}\n'
            f'   │   ├─ Level 1 (Furniture/Kitchen/Decor): 3\n'
            f'   │   └─ Level 2 (Sofas/Cookware/Wall Art etc): {home_living - 3}\n'
            f'   │\n'
            f'   ├─ Books & Education Subcategories: {books_education}\n'
            f'   │   ├─ Level 1 (Academic/Story): 2\n'
            f'   │   └─ Level 2 (Science/Math/Novels etc): {books_education - 2}\n'
            f'   │\n'
            f'   └─ Sports Subcategories: {sports}\n'
            f'       ├─ Level 1 (Cricket/Football/Badminton): 3\n'
            f'       └─ Level 2 (Bats/Balls/Rackets etc): {sports - 3}\n'
        ))