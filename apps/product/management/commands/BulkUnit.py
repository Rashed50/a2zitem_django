import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

##? Models Import
from apps.product.models.unit import UnitOfMeasure

"""
##TODO:- python manage.py BulkUnit
"""
class Command(BaseCommand):
    help = 'Bulk unit of measure creation from predefined data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk unit of measure creation...'))
        
        units = [
            ##! Weight Units
            {"name": "Kilogram", "full_name": "kg"},
            {"name": "Gram", "full_name": "g"},
            {"name": "Milligram", "full_name": "mg"},
            {"name": "Metric Ton", "full_name": "t"},
            {"name": "Pound", "full_name": "lb"},
            {"name": "Ounce", "full_name": "oz"},
            
            ##! Volume Units
            {"name": "Liter", "full_name": "L"},
            {"name": "Milliliter", "full_name": "mL"},
            {"name": "Gallon", "full_name": "gal"},
            {"name": "Quart", "full_name": "qt"},
            {"name": "Pint", "full_name": "pt"},
            {"name": "Fluid Ounce", "full_name": "fl oz"},
            {"name": "Cubic Meter", "full_name": "m³"},
            {"name": "Cubic Centimeter", "full_name": "cm³"},
            
            ##! Length Units
            {"name": "Meter", "full_name": "m"},
            {"name": "Centimeter", "full_name": "cm"},
            {"name": "Millimeter", "full_name": "mm"},
            {"name": "Kilometer", "full_name": "km"},
            {"name": "Inch", "full_name": "in"},
            {"name": "Foot", "full_name": "ft"},
            {"name": "Yard", "full_name": "yd"},
            {"name": "Mile", "full_name": "mi"},
            
            ##! Area Units
            {"name": "Square Meter", "full_name": "m²"},
            {"name": "Square Centimeter", "full_name": "cm²"},
            {"name": "Square Foot", "full_name": "ft²"},
            {"name": "Square Yard", "full_name": "yd²"},
            {"name": "Acre", "full_name": "ac"},
            {"name": "Hectare", "full_name": "ha"},
            
            ##! Piece/Count Units
            {"name": "Piece", "full_name": "pc"},
            {"name": "Pair", "full_name": "pr"},
            {"name": "Set", "full_name": "set"},
            {"name": "Dozen", "full_name": "doz"},
            {"name": "Box", "full_name": "box"},
            {"name": "Pack", "full_name": "pk"},
            {"name": "Carton", "full_name": "ctn"},
            {"name": "Bundle", "full_name": "bdl"},
            {"name": "Roll", "full_name": "roll"},
            {"name": "Sheet", "full_name": "sheet"},
            
            ##! Time Units
            {"name": "Second", "full_name": "s"},
            {"name": "Minute", "full_name": "min"},
            {"name": "Hour", "full_name": "h"},
            {"name": "Day", "full_name": "d"},
            {"name": "Week", "full_name": "wk"},
            {"name": "Month", "full_name": "mo"},
            {"name": "Year", "full_name": "yr"},
            
            ##! Energy Units
            {"name": "Watt", "full_name": "W"},
            {"name": "Kilowatt", "full_name": "kW"},
            {"name": "Megawatt", "full_name": "MW"},
            {"name": "Horsepower", "full_name": "hp"},
            {"name": "Kilowatt-hour", "full_name": "kWh"},
            {"name": "Joule", "full_name": "J"},
            {"name": "Calorie", "full_name": "cal"},
            
            ##! Temperature Units
            {"name": "Celsius", "full_name": "°C"},
            {"name": "Fahrenheit", "full_name": "°F"},
            {"name": "Kelvin", "full_name": "K"},
            
            ##! Pressure Units
            {"name": "Pascal", "full_name": "Pa"},
            {"name": "Kilopascal", "full_name": "kPa"},
            {"name": "Bar", "full_name": "bar"},
            {"name": "PSI", "full_name": "psi"},
            {"name": "Atmosphere", "full_name": "atm"},
            
            ##! Speed Units
            {"name": "Meter per Second", "full_name": "m/s"},
            {"name": "Kilometer per Hour", "full_name": "km/h"},
            {"name": "Mile per Hour", "full_name": "mph"},
            {"name": "Knot", "full_name": "kn"},
            
            ##! Data Storage Units
            {"name": "Byte", "full_name": "B"},
            {"name": "Kilobyte", "full_name": "KB"},
            {"name": "Megabyte", "full_name": "MB"},
            {"name": "Gigabyte", "full_name": "GB"},
            {"name": "Terabyte", "full_name": "TB"},
            {"name": "Petabyte", "full_name": "PB"},
            
            ##! Concentration Units
            {"name": "Percent", "full_name": "%"},
            {"name": "Parts Per Million", "full_name": "ppm"},
            {"name": "Parts Per Billion", "full_name": "ppb"},
            {"name": "Molar", "full_name": "M"},
            {"name": "Millimolar", "full_name": "mM"},
            
            ##! Textile Units
            {"name": "Denier", "full_name": "den"},
            {"name": "Tex", "full_name": "tex"},
            {"name": "Thread Count", "full_name": "TC"},
            {"name": "GSM", "full_name": "gsm"},
            
            ##! Construction Units
            {"name": "Bag", "full_name": "bag"},
            {"name": "Ton", "full_name": "ton"},
            {"name": "Cubic Feet", "full_name": "ft³"},
            {"name": "Board Feet", "full_name": "bdft"},
            {"name": "Square Feet", "full_name": "sq ft"},
            
            ##! Food Industry Units
            {"name": "Cup", "full_name": "cup"},
            {"name": "Tablespoon", "full_name": "tbsp"},
            {"name": "Teaspoon", "full_name": "tsp"},
            {"name": "Pinch", "full_name": "pinch"},
            {"name": "Dash", "full_name": "dash"},
            {"name": "Drop", "full_name": "drop"},
            
            ##! Jewelry Units
            {"name": "Carat", "full_name": "ct"},
            {"name": "Gram", "full_name": "g"},
            {"name": "Tola", "full_name": "tola"},
            {"name": "Bhori", "full_name": "bhori"},
            {"name": "Anna", "full_name": "anna"},
            {"name": "Ratti", "full_name": "ratti"},
            
            ##! Agricultural Units
            {"name": "Kilogram", "full_name": "kg"},
            {"name": "Quintal", "full_name": "q"},
            # {"name": "Ton", "full_name": "t"},
            {"name": "Bale", "full_name": "bale"},
            {"name": "Bushel", "full_name": "bu"},
            {"name": "Sack", "full_name": "sack"},
            
            ##! Paper Units
            {"name": "Ream", "full_name": "ream"},
            {"name": "Quire", "full_name": "quire"},
            {"name": "Sheet", "full_name": "sheet"},
            
            ##! Liquid Units (US/UK)
            {"name": "US Gallon", "full_name": "US gal"},
            {"name": "UK Gallon", "full_name": "UK gal"},
            {"name": "US Quart", "full_name": "US qt"},
            {"name": "UK Quart", "full_name": "UK qt"},
            {"name": "US Pint", "full_name": "US pt"},
            {"name": "UK Pint", "full_name": "UK pt"},
            
            ##! Special Units
            {"name": "Unit", "full_name": "u"},
            {"name": "Each", "full_name": "ea"},
            {"name": "Case", "full_name": "case"},
            {"name": "Pallet", "full_name": "plt"},
            {"name": "Container", "full_name": "cont"},
            {"name": "Drum", "full_name": "drum"},
            {"name": "Can", "full_name": "can"},
            {"name": "Bottle", "full_name": "btl"},
            {"name": "Jar", "full_name": "jar"},
            {"name": "Tube", "full_name": "tube"},
            {"name": "Spool", "full_name": "spool"},
            {"name": "Coil", "full_name": "coil"},
            {"name": "Reel", "full_name": "reel"},
            
            ##! Bangladeshi Local Units
            {"name": "Maund", "full_name": "mn"},
            {"name": "Seer", "full_name": "sr"},
            {"name": "Chhatak", "full_name": "chk"},
            {"name": "Poa", "full_name": "poa"},
            {"name": "Dhoni", "full_name": "dhn"},
            {"name": "Kani", "full_name": "kani"},
            {"name": "Gonda", "full_name": "gnd"},
            {"name": "Kara", "full_name": "kra"},
            {"name": "Ratik", "full_name": "rtk"},
            # {"name": "Tola (BD)", "full_name": "tola"},
            # {"name": "Bhori (BD)", "full_name": "bhori"},
            {"name": "Ana", "full_name": "ana"},
            # {"name": "Ratti (BD)", "full_name": "ratti"},
            {"name": "Dhur", "full_name": "dhur"},
            {"name": "Katha", "full_name": "katha"},
            {"name": "Bigha", "full_name": "bigha"},
            {"name": "Shotok", "full_name": "stk"},
            {"name": "Decimal", "full_name": "dec"},
        ]
        
        # Remove duplicates (if any)
        seen = set()
        unique_units = []
        for unit in units:
            key = (unit["name"], unit["full_name"])
            if key not in seen:
                seen.add(key)
                unique_units.append(unit)
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for unit_data in unique_units:
            try:
                # Create or update unit
                obj, created = UnitOfMeasure.objects.update_or_create(
                    name=unit_data["name"],
                    defaults={
                        "full_name": unit_data["full_name"]
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Created: {unit_data["name"]} ({unit_data["full_name"]})'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'🔄 Updated: {unit_data["name"]} ({unit_data["full_name"]})'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {unit_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk unit of measure creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   └─ Total Units: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Units: {len(unique_units)}\n'
            
            f'\n📋 Unit Categories:\n'
            f'   ├─ Weight Units: 6\n'
            f'   ├─ Volume Units: 8\n'
            f'   ├─ Length Units: 8\n'
            f'   ├─ Area Units: 6\n'
            f'   ├─ Piece/Count Units: 10\n'
            f'   ├─ Time Units: 7\n'
            f'   ├─ Energy Units: 7\n'
            f'   ├─ Temperature Units: 3\n'
            f'   ├─ Pressure Units: 5\n'
            f'   ├─ Speed Units: 4\n'
            f'   ├─ Data Storage Units: 6\n'
            f'   ├─ Concentration Units: 5\n'
            f'   ├─ Textile Units: 4\n'
            f'   ├─ Construction Units: 5\n'
            f'   ├─ Food Industry Units: 6\n'
            f'   ├─ Jewelry Units: 6\n'
            f'   ├─ Agricultural Units: 6\n'
            f'   ├─ Paper Units: 3\n'
            f'   ├─ Liquid Units (US/UK): 6\n'
            f'   ├─ Special Units: 13\n'
            f'   └─ Bangladeshi Local Units: 18\n'
        ))