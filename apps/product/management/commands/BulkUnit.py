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
            {"name": "Kilogram", "symbol": "kg"},
            {"name": "Gram", "symbol": "g"},
            {"name": "Milligram", "symbol": "mg"},
            {"name": "Metric Ton", "symbol": "t"},
            {"name": "Pound", "symbol": "lb"},
            {"name": "Ounce", "symbol": "oz"},
            
            ##! Volume Units
            {"name": "Liter", "symbol": "L"},
            {"name": "Milliliter", "symbol": "mL"},
            {"name": "Gallon", "symbol": "gal"},
            {"name": "Quart", "symbol": "qt"},
            {"name": "Pint", "symbol": "pt"},
            {"name": "Fluid Ounce", "symbol": "fl oz"},
            {"name": "Cubic Meter", "symbol": "m³"},
            {"name": "Cubic Centimeter", "symbol": "cm³"},
            
            ##! Length Units
            {"name": "Meter", "symbol": "m"},
            {"name": "Centimeter", "symbol": "cm"},
            {"name": "Millimeter", "symbol": "mm"},
            {"name": "Kilometer", "symbol": "km"},
            {"name": "Inch", "symbol": "in"},
            {"name": "Foot", "symbol": "ft"},
            {"name": "Yard", "symbol": "yd"},
            {"name": "Mile", "symbol": "mi"},
            
            ##! Area Units
            {"name": "Square Meter", "symbol": "m²"},
            {"name": "Square Centimeter", "symbol": "cm²"},
            {"name": "Square Foot", "symbol": "ft²"},
            {"name": "Square Yard", "symbol": "yd²"},
            {"name": "Acre", "symbol": "ac"},
            {"name": "Hectare", "symbol": "ha"},
            
            ##! Piece/Count Units
            {"name": "Piece", "symbol": "pc"},
            {"name": "Pair", "symbol": "pr"},
            {"name": "Set", "symbol": "set"},
            {"name": "Dozen", "symbol": "doz"},
            {"name": "Box", "symbol": "box"},
            {"name": "Pack", "symbol": "pk"},
            {"name": "Carton", "symbol": "ctn"},
            {"name": "Bundle", "symbol": "bdl"},
            {"name": "Roll", "symbol": "roll"},
            {"name": "Sheet", "symbol": "sheet"},
            
            ##! Time Units
            {"name": "Second", "symbol": "s"},
            {"name": "Minute", "symbol": "min"},
            {"name": "Hour", "symbol": "h"},
            {"name": "Day", "symbol": "d"},
            {"name": "Week", "symbol": "wk"},
            {"name": "Month", "symbol": "mo"},
            {"name": "Year", "symbol": "yr"},
            
            ##! Energy Units
            {"name": "Watt", "symbol": "W"},
            {"name": "Kilowatt", "symbol": "kW"},
            {"name": "Megawatt", "symbol": "MW"},
            {"name": "Horsepower", "symbol": "hp"},
            {"name": "Kilowatt-hour", "symbol": "kWh"},
            {"name": "Joule", "symbol": "J"},
            {"name": "Calorie", "symbol": "cal"},
            
            ##! Temperature Units
            {"name": "Celsius", "symbol": "°C"},
            {"name": "Fahrenheit", "symbol": "°F"},
            {"name": "Kelvin", "symbol": "K"},
            
            ##! Pressure Units
            {"name": "Pascal", "symbol": "Pa"},
            {"name": "Kilopascal", "symbol": "kPa"},
            {"name": "Bar", "symbol": "bar"},
            {"name": "PSI", "symbol": "psi"},
            {"name": "Atmosphere", "symbol": "atm"},
            
            ##! Speed Units
            {"name": "Meter per Second", "symbol": "m/s"},
            {"name": "Kilometer per Hour", "symbol": "km/h"},
            {"name": "Mile per Hour", "symbol": "mph"},
            {"name": "Knot", "symbol": "kn"},
            
            ##! Data Storage Units
            {"name": "Byte", "symbol": "B"},
            {"name": "Kilobyte", "symbol": "KB"},
            {"name": "Megabyte", "symbol": "MB"},
            {"name": "Gigabyte", "symbol": "GB"},
            {"name": "Terabyte", "symbol": "TB"},
            {"name": "Petabyte", "symbol": "PB"},
            
            ##! Concentration Units
            {"name": "Percent", "symbol": "%"},
            {"name": "Parts Per Million", "symbol": "ppm"},
            {"name": "Parts Per Billion", "symbol": "ppb"},
            {"name": "Molar", "symbol": "M"},
            {"name": "Millimolar", "symbol": "mM"},
            
            ##! Textile Units
            {"name": "Denier", "symbol": "den"},
            {"name": "Tex", "symbol": "tex"},
            {"name": "Thread Count", "symbol": "TC"},
            {"name": "GSM", "symbol": "gsm"},
            
            ##! Construction Units
            {"name": "Bag", "symbol": "bag"},
            {"name": "Ton", "symbol": "ton"},
            {"name": "Cubic Feet", "symbol": "ft³"},
            {"name": "Board Feet", "symbol": "bdft"},
            {"name": "Square Feet", "symbol": "sq ft"},
            
            ##! Food Industry Units
            {"name": "Cup", "symbol": "cup"},
            {"name": "Tablespoon", "symbol": "tbsp"},
            {"name": "Teaspoon", "symbol": "tsp"},
            {"name": "Pinch", "symbol": "pinch"},
            {"name": "Dash", "symbol": "dash"},
            {"name": "Drop", "symbol": "drop"},
            
            ##! Jewelry Units
            {"name": "Carat", "symbol": "ct"},
            {"name": "Gram", "symbol": "g"},
            {"name": "Tola", "symbol": "tola"},
            {"name": "Bhori", "symbol": "bhori"},
            {"name": "Anna", "symbol": "anna"},
            {"name": "Ratti", "symbol": "ratti"},
            
            ##! Agricultural Units
            {"name": "Kilogram", "symbol": "kg"},
            {"name": "Quintal", "symbol": "q"},
            # {"name": "Ton", "symbol": "t"},
            {"name": "Bale", "symbol": "bale"},
            {"name": "Bushel", "symbol": "bu"},
            {"name": "Sack", "symbol": "sack"},
            
            ##! Paper Units
            {"name": "Ream", "symbol": "ream"},
            {"name": "Quire", "symbol": "quire"},
            {"name": "Sheet", "symbol": "sheet"},
            
            ##! Liquid Units (US/UK)
            {"name": "US Gallon", "symbol": "US gal"},
            {"name": "UK Gallon", "symbol": "UK gal"},
            {"name": "US Quart", "symbol": "US qt"},
            {"name": "UK Quart", "symbol": "UK qt"},
            {"name": "US Pint", "symbol": "US pt"},
            {"name": "UK Pint", "symbol": "UK pt"},
            
            ##! Special Units
            {"name": "Unit", "symbol": "u"},
            {"name": "Each", "symbol": "ea"},
            {"name": "Case", "symbol": "case"},
            {"name": "Pallet", "symbol": "plt"},
            {"name": "Container", "symbol": "cont"},
            {"name": "Drum", "symbol": "drum"},
            {"name": "Can", "symbol": "can"},
            {"name": "Bottle", "symbol": "btl"},
            {"name": "Jar", "symbol": "jar"},
            {"name": "Tube", "symbol": "tube"},
            {"name": "Spool", "symbol": "spool"},
            {"name": "Coil", "symbol": "coil"},
            {"name": "Reel", "symbol": "reel"},
            
            ##! Bangladeshi Local Units
            {"name": "Maund", "symbol": "mn"},
            {"name": "Seer", "symbol": "sr"},
            {"name": "Chhatak", "symbol": "chk"},
            {"name": "Poa", "symbol": "poa"},
            {"name": "Dhoni", "symbol": "dhn"},
            {"name": "Kani", "symbol": "kani"},
            {"name": "Gonda", "symbol": "gnd"},
            {"name": "Kara", "symbol": "kra"},
            {"name": "Ratik", "symbol": "rtk"},
            # {"name": "Tola (BD)", "symbol": "tola"},
            # {"name": "Bhori (BD)", "symbol": "bhori"},
            {"name": "Ana", "symbol": "ana"},
            # {"name": "Ratti (BD)", "symbol": "ratti"},
            {"name": "Dhur", "symbol": "dhur"},
            {"name": "Katha", "symbol": "katha"},
            {"name": "Bigha", "symbol": "bigha"},
            {"name": "Shotok", "symbol": "stk"},
            {"name": "Decimal", "symbol": "dec"},
        ]
        
        # Remove duplicates (if any)
        seen = set()
        unique_units = []
        for unit in units:
            key = (unit["name"], unit["symbol"])
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
                        "symbol": unit_data["symbol"]
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Created: {unit_data["name"]} ({unit_data["symbol"]})'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'🔄 Updated: {unit_data["name"]} ({unit_data["symbol"]})'))
                    
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