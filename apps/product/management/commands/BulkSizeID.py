import json
import os
import random
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

##? Models Import
from apps.product.models.size import Size
from apps.product.management.commands.data.sizesDataSheet import sizes_data

"""
##TODO:- python manage.py BulkSizeID
"""
class Command(BaseCommand):
    help = 'Bulk size creation from predefined data'
    
    def generate_random_id(self, min_id=1001, max_id=9999):
        """Generate random ID between min_id and max_id"""
        return random.randint(min_id, max_id)
    
    def get_unique_id(self, preferred_id=None, min_id=1001, max_id=9999):
        """
        Get a unique ID for size.
        If preferred_id is provided and not taken, use it.
        Otherwise generate random unique ID.
        """
        if preferred_id:
            # Check if preferred_id is available
            if not Size.objects.filter(id=preferred_id).exists():
                return preferred_id
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Preferred ID {preferred_id} is taken, generating random ID'))
        
        # Generate random unique ID
        while True:
            random_id = self.generate_random_id(min_id, max_id)
            if not Size.objects.filter(id=random_id).exists():
                return random_id
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk size creation with custom IDs...'))
        
        sizes = sizes_data
        
        # Remove duplicates while preserving order
        seen_names = set()
        seen_ids = set()
        unique_sizes = []
        
        for size in sizes:
            if size["name"] not in seen_names:
                # Check for duplicate preferred IDs
                if size["preferred_id"] in seen_ids:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ Duplicate preferred ID {size["preferred_id"]} for {size["name"]}, will generate random ID'
                    ))
                    size["preferred_id"] = None  # Will generate random
                
                seen_names.add(size["name"])
                if size["preferred_id"]:
                    seen_ids.add(size["preferred_id"])
                unique_sizes.append(size)
        
        self.stdout.write(self.style.WARNING(f'Total sizes to process: {len(unique_sizes)}'))
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        id_conflicts = 0
        
        for size_data in unique_sizes:
            try:
                # Get unique ID (preferred or random)
                final_id = self.get_unique_id(size_data.get("preferred_id"))
                
                if size_data.get("preferred_id") and size_data["preferred_id"] != final_id:
                    id_conflicts += 1
                
                # Try to create with specific ID
                try:
                    # Create size with specific ID
                    size = Size(id=final_id, name=size_data["name"])
                    size.save()
                    created_count += 1
                    
                    # Show first 20 creations with details
                    if created_count <= 20:
                        id_info = f"(ID: {final_id}"
                        if size_data.get("preferred_id"):
                            if size_data["preferred_id"] == final_id:
                                id_info += f" - preferred: {size_data['preferred_id']}"
                            else:
                                id_info += f" - preferred: {size_data['preferred_id']} was taken)"
                        else:
                            id_info += " - random)"
                        
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {size_data["name"]:25} {id_info}'))
                    
                except IntegrityError:
                    # If ID exists, create with new ID
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ ID {final_id} for {size_data["name"]} was taken in between, retrying...'
                    ))
                    
                    # Get another unique ID
                    new_id = self.get_unique_id(min_id=1001, max_id=9999)
                    size = Size(id=new_id, name=size_data["name"])
                    size.save()
                    created_count += 1
                    
                    if created_count <= 20:
                        self.stdout.write(self.style.SUCCESS(
                            f'✅ Created: {size_data["name"]:25} (ID: {new_id} - random after conflict)'
                        ))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {size_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        # Category wise count
        general_clothing = len([s for s in unique_sizes if s["preferred_id"] and s["preferred_id"] <= 10])
        numeric_clothing = len([s for s in unique_sizes if 11 <= (s["preferred_id"] or 0) <= 41])
        kids_sizes = len([s for s in unique_sizes if 42 <= (s["preferred_id"] or 0) <= 61])
        womens_sizes = len([s for s in unique_sizes if 62 <= (s["preferred_id"] or 0) <= 72])
        mens_sizes = len([s for s in unique_sizes if 73 <= (s["preferred_id"] or 0) <= 81])
        shoe_sizes = len([s for s in unique_sizes if 82 <= (s["preferred_id"] or 0) <= 137])
        jeans_sizes = len([s for s in unique_sizes if 138 <= (s["preferred_id"] or 0) <= 160])
        bra_sizes = len([s for s in unique_sizes if 161 <= (s["preferred_id"] or 0) <= 185])
        ring_hat_glove = len([s for s in unique_sizes if 186 <= (s["preferred_id"] or 0) <= 225])
        belt_sizes = len([s for s in unique_sizes if 226 <= (s["preferred_id"] or 0) <= 234])
        plus_petite_tall = len([s for s in unique_sizes if 235 <= (s["preferred_id"] or 0) <= 262])
        uniform_sizes = len([s for s in unique_sizes if 263 <= (s["preferred_id"] or 0) <= 280])
        sock_tights = len([s for s in unique_sizes if 281 <= (s["preferred_id"] or 0) <= 295])
        asian_sizes = len([s for s in unique_sizes if 296 <= (s["preferred_id"] or 0) <= 302])
        eu_uk_us = len([s for s in unique_sizes if 303 <= (s["preferred_id"] or 0) <= 338])
        intl_sizes = len([s for s in unique_sizes if 339 <= (s["preferred_id"] or 0) <= 353])
        home_sizes = len([s for s in unique_sizes if 354 <= (s["preferred_id"] or 0) <= 370])
        paper_photo = len([s for s in unique_sizes if 371 <= (s["preferred_id"] or 0) <= 397])
        screen_sizes = len([s for s in unique_sizes if 398 <= (s["preferred_id"] or 0) <= 417])
        luggage_bottle = len([s for s in unique_sizes if 418 <= (s["preferred_id"] or 0) <= 438])
        bangladeshi = len([s for s in unique_sizes if 439 <= (s["preferred_id"] or 0) <= 465])
        custom = len([s for s in unique_sizes if 466 <= (s["preferred_id"] or 0) <= 469])
        numeric_ranges = len([s for s in unique_sizes if 470 <= (s["preferred_id"] or 0) <= 481])
        universal = len([s for s in unique_sizes if 482 <= (s["preferred_id"] or 0) <= 485])
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk size creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   ├─ ID Conflicts Resolved: {id_conflicts}\n'
            f'   └─ Total Sizes: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Sizes: {len(unique_sizes)}\n'
            
            f'\n📋 Size Categories:\n'
            f'   ├─ General Clothing: {general_clothing}\n'
            f'   ├─ Numeric Clothing: {numeric_clothing}\n'
            f'   ├─ Kids Sizes: {kids_sizes}\n'
            f'   ├─ Women\'s Sizes: {womens_sizes}\n'
            f'   ├─ Men\'s Sizes: {mens_sizes}\n'
            f'   ├─ Shoe Sizes (US/UK/EU/Kids): {shoe_sizes}\n'
            f'   ├─ Jeans Sizes: {jeans_sizes}\n'
            f'   ├─ Bra Sizes: {bra_sizes}\n'
            f'   ├─ Ring/Hat/Glove Sizes: {ring_hat_glove}\n'
            f'   ├─ Belt Sizes: {belt_sizes}\n'
            f'   ├─ Plus/Petite/Tall/Big: {plus_petite_tall}\n'
            f'   ├─ Uniform Sizes: {uniform_sizes}\n'
            f'   ├─ Sock/Tights: {sock_tights}\n'
            f'   ├─ Asian Sizes: {asian_sizes}\n'
            f'   ├─ EU/UK/US Sizes: {eu_uk_us}\n'
            f'   ├─ International/Unisex: {intl_sizes}\n'
            f'   ├─ Home (Bed/Towel): {home_sizes}\n'
            f'   ├─ Paper/Photo/Frame: {paper_photo}\n'
            f'   ├─ Screen Sizes: {screen_sizes}\n'
            f'   ├─ Luggage/Bottle: {luggage_bottle}\n'
            f'   ├─ Bangladeshi Local: {bangladeshi}\n'
            f'   ├─ Custom/Bespoke: {custom}\n'
            f'   ├─ Numeric Ranges: {numeric_ranges}\n'
            f'   └─ Universal/General: {universal}\n'
        ))