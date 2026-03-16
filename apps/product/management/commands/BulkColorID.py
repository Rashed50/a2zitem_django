import json
import os
import random
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

##? Models Import
from apps.product.models.color import Color
from apps.product.management.commands.data.colorsDataSheet import colors_data

"""
##TODO:- python manage.py BulkColorID
"""
class Command(BaseCommand):
    help = 'Bulk color creation from predefined data'
    
    def generate_random_id(self, min_id=1001, max_id=9999):
        """Generate random ID between min_id and max_id"""
        return random.randint(min_id, max_id)
    
    def get_unique_id(self, preferred_id=None, min_id=1001, max_id=9999):
        """
        Get a unique ID for color.
        If preferred_id is provided and not taken, use it.
        Otherwise generate random unique ID.
        """
        if preferred_id:
            # Check if preferred_id is available
            if not Color.objects.filter(id=preferred_id).exists():
                return preferred_id
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Preferred ID {preferred_id} is taken, generating random ID'))
        
        # Generate random unique ID
        while True:
            random_id = self.generate_random_id(min_id, max_id)
            if not Color.objects.filter(id=random_id).exists():
                return random_id
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk color creation with custom IDs...'))
        
        colors = colors_data
        
        # Remove duplicates while preserving order
        seen_names = set()
        seen_ids = set()
        unique_colors = []
        
        for color in colors:
            if color["name"] not in seen_names:
                # Check for duplicate preferred IDs
                if color["preferred_id"] in seen_ids:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ Duplicate preferred ID {color["preferred_id"]} for {color["name"]}, will generate random ID'
                    ))
                    color["preferred_id"] = None  # Will generate random
                
                seen_names.add(color["name"])
                if color["preferred_id"]:
                    seen_ids.add(color["preferred_id"])
                unique_colors.append(color)
        
        self.stdout.write(self.style.WARNING(f'Total colors to process: {len(unique_colors)}'))
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        id_conflicts = 0
        
        for color_data in unique_colors:
            try:
                # Get unique ID (preferred or random)
                final_id = self.get_unique_id(color_data.get("preferred_id"))
                
                if color_data.get("preferred_id") and color_data["preferred_id"] != final_id:
                    id_conflicts += 1
                
                # Try to create with specific ID
                try:
                    # Create color with specific ID
                    color = Color(id=final_id, name=color_data["name"])
                    color.save()
                    created_count += 1
                    
                    # Show first 20 creations with details
                    if created_count <= 20:
                        id_info = f"(ID: {final_id}"
                        if color_data.get("preferred_id"):
                            if color_data["preferred_id"] == final_id:
                                id_info += f" - preferred: {color_data['preferred_id']}"
                            else:
                                id_info += f" - preferred: {color_data['preferred_id']} was taken)"
                        else:
                            id_info += " - random)"
                        
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {color_data["name"]:25} {id_info}'))
                    
                except IntegrityError:
                    # If ID exists, create with new ID
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ ID {final_id} for {color_data["name"]} was taken in between, retrying...'
                    ))
                    
                    # Get another unique ID
                    new_id = self.get_unique_id(min_id=1001, max_id=9999)
                    color = Color(id=new_id, name=color_data["name"])
                    color.save()
                    created_count += 1
                    
                    if created_count <= 20:
                        self.stdout.write(self.style.SUCCESS(
                            f'✅ Created: {color_data["name"]:25} (ID: {new_id} - random after conflict)'
                        ))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {color_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        # Category wise count
        basic_colors = len([c for c in unique_colors if c["preferred_id"] and c["preferred_id"] <= 54])
        gray_colors = len([c for c in unique_colors if 55 <= (c["preferred_id"] or 0) <= 63])
        metallic_colors = len([c for c in unique_colors if 64 <= (c["preferred_id"] or 0) <= 72])
        pastel_colors = len([c for c in unique_colors if 73 <= (c["preferred_id"] or 0) <= 81])
        neon_colors = len([c for c in unique_colors if 82 <= (c["preferred_id"] or 0) <= 90])
        skin_tones = len([c for c in unique_colors if 91 <= (c["preferred_id"] or 0) <= 98])
        hair_colors = len([c for c in unique_colors if 99 <= (c["preferred_id"] or 0) <= 114])
        eye_colors = len([c for c in unique_colors if 115 <= (c["preferred_id"] or 0) <= 120])
        gemstone_colors = len([c for c in unique_colors if 121 <= (c["preferred_id"] or 0) <= 129])
        food_colors = len([c for c in unique_colors if 130 <= (c["preferred_id"] or 0) <= 147])
        nature_colors = len([c for c in unique_colors if 148 <= (c["preferred_id"] or 0) <= 162])
        flower_colors = len([c for c in unique_colors if 163 <= (c["preferred_id"] or 0) <= 170])
        fabric_colors = len([c for c in unique_colors if 171 <= (c["preferred_id"] or 0) <= 178])
        print_pattern = len([c for c in unique_colors if 179 <= (c["preferred_id"] or 0) <= 191])
        multicolor = len([c for c in unique_colors if 192 <= (c["preferred_id"] or 0) <= 195])
        transparent = len([c for c in unique_colors if 196 <= (c["preferred_id"] or 0) <= 210])
        bangladeshi = len([c for c in unique_colors if 211 <= (c["preferred_id"] or 0) <= 245])
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk color creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   ├─ ID Conflicts Resolved: {id_conflicts}\n'
            f'   └─ Total Colors: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Colors: {len(unique_colors)}\n'
            
            f'\n📋 Color Categories:\n'
            f'   ├─ Basic Colors: {basic_colors}\n'
            f'   ├─ Shades of Gray: {gray_colors}\n'
            f'   ├─ Metallic Colors: {metallic_colors}\n'
            f'   ├─ Pastel Colors: {pastel_colors}\n'
            f'   ├─ Neon Colors: {neon_colors}\n'
            f'   ├─ Skin Tones: {skin_tones}\n'
            f'   ├─ Hair Colors: {hair_colors}\n'
            f'   ├─ Eye Colors: {eye_colors}\n'
            f'   ├─ Gemstone Colors: {gemstone_colors}\n'
            f'   ├─ Food Colors: {food_colors}\n'
            f'   ├─ Nature Colors: {nature_colors}\n'
            f'   ├─ Flower Colors: {flower_colors}\n'
            f'   ├─ Fabric Colors: {fabric_colors}\n'
            f'   ├─ Print/Pattern: {print_pattern}\n'
            f'   ├─ Multicolor: {multicolor}\n'
            f'   ├─ Transparent/Effect: {transparent}\n'
            f'   └─ Bangladeshi Colors: {bangladeshi}\n'
        ))