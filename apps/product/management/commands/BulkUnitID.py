import json
import os
import random
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError

##? Models Import
from apps.product.models.unit import UnitOfMeasure
from apps.product.management.commands.data.unitsDataSheet import units_data

"""
##TODO:- python manage.py BulkUnitID
"""
class Command(BaseCommand):
    help = 'Bulk unit of measure creation from predefined data'
    
    def generate_random_id(self, min_id=1001, max_id=9999):
        """Generate random ID between min_id and max_id"""
        return random.randint(min_id, max_id)
    
    def get_unique_id(self, preferred_id=None, min_id=1001, max_id=9999):
        """
        Get a unique ID for unit.
        If preferred_id is provided and not taken, use it.
        Otherwise generate random unique ID.
        """
        if preferred_id:
            # Check if preferred_id is available
            if not UnitOfMeasure.objects.filter(id=preferred_id).exists():
                return preferred_id
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Preferred ID {preferred_id} is taken, generating random ID'))
        
        # Generate random unique ID
        while True:
            random_id = self.generate_random_id(min_id, max_id)
            if not UnitOfMeasure.objects.filter(id=random_id).exists():
                return random_id
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk unit of measure creation with custom IDs...'))
        
        units = units_data
        
        # Remove duplicates while preserving order
        seen_keys = set()
        seen_ids = set()
        unique_units = []
        
        for unit in units:
            key = (unit["name"], unit["symbol"])
            if key not in seen_keys:
                # Check for duplicate preferred IDs
                if unit["preferred_id"] in seen_ids:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ Duplicate preferred ID {unit["preferred_id"]} for {unit["name"]} ({unit["symbol"]}), will generate random ID'
                    ))
                    unit["preferred_id"] = None  # Will generate random
                
                seen_keys.add(key)
                if unit["preferred_id"]:
                    seen_ids.add(unit["preferred_id"])
                unique_units.append(unit)
        
        self.stdout.write(self.style.WARNING(f'Total units to process: {len(unique_units)}'))
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        id_conflicts = 0
        
        for unit_data in unique_units:
            try:
                # Get unique ID (preferred or random)
                final_id = self.get_unique_id(unit_data.get("preferred_id"))
                
                if unit_data.get("preferred_id") and unit_data["preferred_id"] != final_id:
                    id_conflicts += 1
                
                # Try to create with specific ID
                try:
                    # Create unit with specific ID
                    unit = UnitOfMeasure(
                        id=final_id, 
                        name=unit_data["name"],
                        symbol=unit_data["symbol"]
                    )
                    unit.save()
                    created_count += 1
                    
                    # Show first 20 creations with details
                    if created_count <= 20:
                        id_info = f"(ID: {final_id}"
                        if unit_data.get("preferred_id"):
                            if unit_data["preferred_id"] == final_id:
                                id_info += f" - preferred: {unit_data['preferred_id']}"
                            else:
                                id_info += f" - preferred: {unit_data['preferred_id']} was taken)"
                        else:
                            id_info += " - random)"
                        
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {unit_data["name"]:25} ({unit_data["symbol"]:6}) {id_info}'))
                    
                except IntegrityError:
                    # If ID exists, create with new ID
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ ID {final_id} for {unit_data["name"]} was taken in between, retrying...'
                    ))
                    
                    # Get another unique ID
                    new_id = self.get_unique_id(min_id=1001, max_id=9999)
                    unit = UnitOfMeasure(
                        id=new_id,
                        name=unit_data["name"],
                        symbol=unit_data["symbol"]
                    )
                    unit.save()
                    created_count += 1
                    
                    if created_count <= 20:
                        self.stdout.write(self.style.SUCCESS(
                            f'✅ Created: {unit_data["name"]:25} ({unit_data["symbol"]:6}) (ID: {new_id} - random after conflict)'
                        ))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {unit_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        # Category wise count
        weight_units = len([u for u in unique_units if u["preferred_id"] and u["preferred_id"] <= 6])
        volume_units = len([u for u in unique_units if 7 <= (u["preferred_id"] or 0) <= 14])
        length_units = len([u for u in unique_units if 15 <= (u["preferred_id"] or 0) <= 22])
        area_units = len([u for u in unique_units if 23 <= (u["preferred_id"] or 0) <= 28])
        piece_units = len([u for u in unique_units if 29 <= (u["preferred_id"] or 0) <= 38])
        time_units = len([u for u in unique_units if 39 <= (u["preferred_id"] or 0) <= 45])
        energy_units = len([u for u in unique_units if 46 <= (u["preferred_id"] or 0) <= 52])
        temp_units = len([u for u in unique_units if 53 <= (u["preferred_id"] or 0) <= 55])
        pressure_units = len([u for u in unique_units if 56 <= (u["preferred_id"] or 0) <= 60])
        speed_units = len([u for u in unique_units if 61 <= (u["preferred_id"] or 0) <= 64])
        data_units = len([u for u in unique_units if 65 <= (u["preferred_id"] or 0) <= 70])
        concentration_units = len([u for u in unique_units if 71 <= (u["preferred_id"] or 0) <= 75])
        textile_units = len([u for u in unique_units if 76 <= (u["preferred_id"] or 0) <= 79])
        construction_units = len([u for u in unique_units if 80 <= (u["preferred_id"] or 0) <= 84])
        food_units = len([u for u in unique_units if 85 <= (u["preferred_id"] or 0) <= 90])
        jewelry_units = len([u for u in unique_units if 91 <= (u["preferred_id"] or 0) <= 96])
        agri_units = len([u for u in unique_units if 97 <= (u["preferred_id"] or 0) <= 102])
        paper_units = len([u for u in unique_units if 103 <= (u["preferred_id"] or 0) <= 105])
        liquid_units = len([u for u in unique_units if 106 <= (u["preferred_id"] or 0) <= 111])
        special_units = len([u for u in unique_units if 112 <= (u["preferred_id"] or 0) <= 124])
        bangladeshi_units = len([u for u in unique_units if 125 <= (u["preferred_id"] or 0) <= 142])
        additional_volume = len([u for u in unique_units if 143 <= (u["preferred_id"] or 0) <= 147])
        additional_weight = len([u for u in unique_units if 148 <= (u["preferred_id"] or 0) <= 152])
        electrical_units = len([u for u in unique_units if 153 <= (u["preferred_id"] or 0) <= 157])
        frequency_units = len([u for u in unique_units if 158 <= (u["preferred_id"] or 0) <= 160])
        luminosity_units = len([u for u in unique_units if 161 <= (u["preferred_id"] or 0) <= 163])
        radioactivity_units = len([u for u in unique_units if 164 <= (u["preferred_id"] or 0) <= 166])
        chemistry_units = len([u for u in unique_units if 167 <= (u["preferred_id"] or 0) <= 169])
        typography_units = len([u for u in unique_units if 170 <= (u["preferred_id"] or 0) <= 172])
        angular_units = len([u for u in unique_units if 173 <= (u["preferred_id"] or 0) <= 175])
        force_units = len([u for u in unique_units if 176 <= (u["preferred_id"] or 0) <= 178])
        torque_units = len([u for u in unique_units if 179 <= (u["preferred_id"] or 0) <= 181])
        flow_units = len([u for u in unique_units if 182 <= (u["preferred_id"] or 0) <= 185])
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk unit of measure creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   ├─ ID Conflicts Resolved: {id_conflicts}\n'
            f'   └─ Total Units: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Units: {len(unique_units)}\n'
            
            f'\n📋 Unit Categories:\n'
            f'   ├─ Weight Units: {weight_units}\n'
            f'   ├─ Volume Units: {volume_units}\n'
            f'   ├─ Length Units: {length_units}\n'
            f'   ├─ Area Units: {area_units}\n'
            f'   ├─ Piece/Count Units: {piece_units}\n'
            f'   ├─ Time Units: {time_units}\n'
            f'   ├─ Energy Units: {energy_units}\n'
            f'   ├─ Temperature Units: {temp_units}\n'
            f'   ├─ Pressure Units: {pressure_units}\n'
            f'   ├─ Speed Units: {speed_units}\n'
            f'   ├─ Data Storage Units: {data_units}\n'
            f'   ├─ Concentration Units: {concentration_units}\n'
            f'   ├─ Textile Units: {textile_units}\n'
            f'   ├─ Construction Units: {construction_units}\n'
            f'   ├─ Food Industry Units: {food_units}\n'
            f'   ├─ Jewelry Units: {jewelry_units}\n'
            f'   ├─ Agricultural Units: {agri_units}\n'
            f'   ├─ Paper Units: {paper_units}\n'
            f'   ├─ Liquid Units (US/UK): {liquid_units}\n'
            f'   ├─ Special Units: {special_units}\n'
            f'   ├─ Bangladeshi Local Units: {bangladeshi_units}\n'
            f'   ├─ Additional Volume: {additional_volume}\n'
            f'   ├─ Additional Weight: {additional_weight}\n'
            f'   ├─ Electrical Units: {electrical_units}\n'
            f'   ├─ Frequency Units: {frequency_units}\n'
            f'   ├─ Luminosity Units: {luminosity_units}\n'
            f'   ├─ Radioactivity Units: {radioactivity_units}\n'
            f'   ├─ Chemistry Units: {chemistry_units}\n'
            f'   ├─ Typography Units: {typography_units}\n'
            f'   ├─ Angular Units: {angular_units}\n'
            f'   ├─ Force Units: {force_units}\n'
            f'   ├─ Torque Units: {torque_units}\n'
            f'   └─ Flow Rate Units: {flow_units}\n'
        ))