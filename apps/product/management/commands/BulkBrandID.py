import json
import os
import random
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

##? Models Import
from apps.product.models.brand import Brand
from apps.product.management.commands.data.brandDataSheet import brands_data

"""
##TODO:- python manage.py BulkBrandID
"""
class Command(BaseCommand):
    help = 'Bulk brand creation from predefined data'
    
    def generate_random_id(self, min_id=1001, max_id=9999):
        """Generate random ID between min_id and max_id"""
        return random.randint(min_id, max_id)
    
    def get_unique_id(self, preferred_id=None, min_id=1001, max_id=9999):
        """
        Get a unique ID for brand.
        If preferred_id is provided and not taken, use it.
        Otherwise generate random unique ID.
        """
        if preferred_id:
            # Check if preferred_id is available
            if not Brand.objects.filter(id=preferred_id).exists():
                return preferred_id
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Preferred ID {preferred_id} is taken, generating random ID'))
        
        # Generate random unique ID
        while True:
            random_id = self.generate_random_id(min_id, max_id)
            if not Brand.objects.filter(id=random_id).exists():
                return random_id
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk brand creation with custom IDs...'))
        
        brands = brands_data
        
        # Remove duplicates while preserving order
        seen_names = set()
        seen_ids = set()
        unique_brands = []
        
        for brand in brands:
            if brand["name"] not in seen_names:
                # Check for duplicate preferred IDs
                if brand["preferred_id"] in seen_ids:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ Duplicate preferred ID {brand["preferred_id"]} for {brand["name"]}, will generate random ID'
                    ))
                    brand["preferred_id"] = None  # Will generate random
                
                seen_names.add(brand["name"])
                if brand["preferred_id"]:
                    seen_ids.add(brand["preferred_id"])
                unique_brands.append(brand)
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        id_conflicts = 0
        
        for brand_data in unique_brands:
            try:
                # Get unique ID (preferred or random)
                final_id = self.get_unique_id(brand_data.get("preferred_id"))
                
                if brand_data.get("preferred_id") and brand_data["preferred_id"] != final_id:
                    id_conflicts += 1
                
                # Try to create with specific ID
                try:
                    # Create brand with specific ID
                    brand = Brand(id=final_id, name=brand_data["name"])
                    brand.save()
                    created_count += 1
                    id_info = f"(ID: {final_id}"
                    if brand_data.get("preferred_id"):
                        if brand_data["preferred_id"] == final_id:
                            id_info += f" - preferred: {brand_data['preferred_id']}"
                        else:
                            id_info += f" - preferred: {brand_data['preferred_id']} was taken)"
                    else:
                        id_info += " - random)"
                    
                    self.stdout.write(self.style.SUCCESS(f'✅ Created: {brand_data["name"]} {id_info}'))
                    
                except IntegrityError:
                    # If ID exists, update or create with new ID
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ ID {final_id} for {brand_data["name"]} was taken in between, retrying...'
                    ))
                    
                    # Get another unique ID
                    new_id = self.get_unique_id(min_id=1001, max_id=9999)
                    brand = Brand(id=new_id, name=brand_data["name"])
                    brand.save()
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ Created: {brand_data["name"]} (ID: {new_id} - random after conflict)'
                    ))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {brand_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk brand creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   ├─ ID Conflicts Resolved: {id_conflicts}\n'
            f'   └─ Total Brands: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Brands: {len(unique_brands)}\n'
        ))