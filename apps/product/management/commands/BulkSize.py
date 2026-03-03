import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

##? Models Import
from apps.product.models.size import Size

"""
##TODO:- python manage.py BulkSize
"""
class Command(BaseCommand):
    help = 'Bulk size creation from predefined data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk size creation...'))
        
        sizes = [
            # Clothing Sizes - General
            {"name": "XXS"},
            {"name": "XS"},
            {"name": "S"},
            {"name": "M"},
            {"name": "L"},
            {"name": "XL"},
            {"name": "XXL"},
            {"name": "XXXL"},
            {"name": "XXXXL"},
            {"name": "XXXXXL"},
            
            # Clothing Sizes - Numeric (US/UK/EU)
            {"name": "0"},
            {"name": "2"},
            {"name": "4"},
            {"name": "6"},
            {"name": "8"},
            {"name": "10"},
            {"name": "12"},
            {"name": "14"},
            {"name": "16"},
            {"name": "18"},
            {"name": "20"},
            {"name": "22"},
            {"name": "24"},
            {"name": "26"},
            {"name": "28"},
            {"name": "30"},
            {"name": "32"},
            {"name": "34"},
            {"name": "36"},
            {"name": "38"},
            {"name": "40"},
            {"name": "42"},
            {"name": "44"},
            {"name": "46"},
            {"name": "48"},
            {"name": "50"},
            {"name": "52"},
            {"name": "54"},
            {"name": "56"},
            {"name": "58"},
            {"name": "60"},
            
            # Kids Sizes
            {"name": "Newborn"},
            {"name": "0-3 Months"},
            {"name": "3-6 Months"},
            {"name": "6-9 Months"},
            {"name": "9-12 Months"},
            {"name": "12-18 Months"},
            {"name": "18-24 Months"},
            {"name": "2T"},
            {"name": "3T"},
            {"name": "4T"},
            {"name": "5T"},
            {"name": "4"},
            {"name": "5"},
            {"name": "6"},
            {"name": "7"},
            {"name": "8"},
            {"name": "10"},
            {"name": "12"},
            {"name": "14"},
            {"name": "16"},
            
            # Women's Sizes - Dress
            {"name": "Women's 0"},
            {"name": "Women's 2"},
            {"name": "Women's 4"},
            {"name": "Women's 6"},
            {"name": "Women's 8"},
            {"name": "Women's 10"},
            {"name": "Women's 12"},
            {"name": "Women's 14"},
            {"name": "Women's 16"},
            {"name": "Women's 18"},
            {"name": "Women's 20"},
            
            # Men's Sizes - Suit
            {"name": "Men's 34"},
            {"name": "Men's 36"},
            {"name": "Men's 38"},
            {"name": "Men's 40"},
            {"name": "Men's 42"},
            {"name": "Men's 44"},
            {"name": "Men's 46"},
            {"name": "Men's 48"},
            {"name": "Men's 50"},
            
            # Shoe Sizes - US
            {"name": "US 4"},
            {"name": "US 5"},
            {"name": "US 6"},
            {"name": "US 7"},
            {"name": "US 8"},
            {"name": "US 9"},
            {"name": "US 10"},
            {"name": "US 11"},
            {"name": "US 12"},
            {"name": "US 13"},
            {"name": "US 14"},
            {"name": "US 15"},
            {"name": "US 16"},
            
            # Shoe Sizes - UK
            {"name": "UK 3"},
            {"name": "UK 4"},
            {"name": "UK 5"},
            {"name": "UK 6"},
            {"name": "UK 7"},
            {"name": "UK 8"},
            {"name": "UK 9"},
            {"name": "UK 10"},
            {"name": "UK 11"},
            {"name": "UK 12"},
            {"name": "UK 13"},
            
            # Shoe Sizes - EU
            {"name": "EU 35"},
            {"name": "EU 36"},
            {"name": "EU 37"},
            {"name": "EU 38"},
            {"name": "EU 39"},
            {"name": "EU 40"},
            {"name": "EU 41"},
            {"name": "EU 42"},
            {"name": "EU 43"},
            {"name": "EU 44"},
            {"name": "EU 45"},
            {"name": "EU 46"},
            {"name": "EU 47"},
            {"name": "EU 48"},
            
            # Kids Shoe Sizes
            {"name": "Kids US 1"},
            {"name": "Kids US 2"},
            {"name": "Kids US 3"},
            {"name": "Kids US 4"},
            {"name": "Kids US 5"},
            {"name": "Kids US 6"},
            {"name": "Kids US 7"},
            {"name": "Kids US 8"},
            {"name": "Kids US 9"},
            {"name": "Kids US 10"},
            {"name": "Kids US 11"},
            {"name": "Kids US 12"},
            {"name": "Kids US 13"},
            
            # Infant Shoe Sizes
            {"name": "Infant US 0"},
            {"name": "Infant US 1"},
            {"name": "Infant US 2"},
            {"name": "Infant US 3"},
            {"name": "Infant US 4"},
            
            # Jeans Sizes - Waist
            {"name": "24W"},
            {"name": "25W"},
            {"name": "26W"},
            {"name": "27W"},
            {"name": "28W"},
            {"name": "29W"},
            {"name": "30W"},
            {"name": "31W"},
            {"name": "32W"},
            {"name": "33W"},
            {"name": "34W"},
            {"name": "35W"},
            {"name": "36W"},
            {"name": "38W"},
            {"name": "40W"},
            {"name": "42W"},
            {"name": "44W"},
            
            # Jeans Sizes - Length/Inseam
            {"name": "28L"},
            {"name": "30L"},
            {"name": "32L"},
            {"name": "34L"},
            {"name": "36L"},
            {"name": "38L"},
            
            # Bra Sizes - Band
            {"name": "28 Band"},
            {"name": "30 Band"},
            {"name": "32 Band"},
            {"name": "34 Band"},
            {"name": "36 Band"},
            {"name": "38 Band"},
            {"name": "40 Band"},
            {"name": "42 Band"},
            {"name": "44 Band"},
            {"name": "46 Band"},
            {"name": "48 Band"},
            
            # Bra Sizes - Cup
            {"name": "AA Cup"},
            {"name": "A Cup"},
            {"name": "B Cup"},
            {"name": "C Cup"},
            {"name": "D Cup"},
            {"name": "DD Cup"},
            {"name": "E Cup"},
            {"name": "F Cup"},
            {"name": "FF Cup"},
            {"name": "G Cup"},
            {"name": "GG Cup"},
            {"name": "H Cup"},
            {"name": "HH Cup"},
            {"name": "J Cup"},
            
            # Ring Sizes
            {"name": "Ring Size 3"},
            {"name": "Ring Size 4"},
            {"name": "Ring Size 5"},
            {"name": "Ring Size 6"},
            {"name": "Ring Size 7"},
            {"name": "Ring Size 8"},
            {"name": "Ring Size 9"},
            {"name": "Ring Size 10"},
            {"name": "Ring Size 11"},
            {"name": "Ring Size 12"},
            {"name": "Ring Size 13"},
            
            # Hat Sizes
            {"name": "Hat - XS"},
            {"name": "Hat - S"},
            {"name": "Hat - M"},
            {"name": "Hat - L"},
            {"name": "Hat - XL"},
            {"name": "Hat - 6 5/8"},
            {"name": "Hat - 6 3/4"},
            {"name": "Hat - 6 7/8"},
            {"name": "Hat - 7"},
            {"name": "Hat - 7 1/8"},
            {"name": "Hat - 7 1/4"},
            {"name": "Hat - 7 3/8"},
            {"name": "Hat - 7 1/2"},
            {"name": "Hat - 7 5/8"},
            {"name": "Hat - 7 3/4"},
            {"name": "Hat - 7 7/8"},
            {"name": "Hat - 8"},
            
            # Glove Sizes
            {"name": "Glove - XS"},
            {"name": "Glove - S"},
            {"name": "Glove - M"},
            {"name": "Glove - L"},
            {"name": "Glove - XL"},
            {"name": "Glove - 6"},
            {"name": "Glove - 7"},
            {"name": "Glove - 8"},
            {"name": "Glove - 9"},
            {"name": "Glove - 10"},
            {"name": "Glove - 11"},
            
            # Belt Sizes
            {"name": "Belt 28"},
            {"name": "Belt 30"},
            {"name": "Belt 32"},
            {"name": "Belt 34"},
            {"name": "Belt 36"},
            {"name": "Belt 38"},
            {"name": "Belt 40"},
            {"name": "Belt 42"},
            {"name": "Belt 44"},
            
            # Plus Sizes
            {"name": "1X"},
            {"name": "2X"},
            {"name": "3X"},
            {"name": "4X"},
            {"name": "5X"},
            {"name": "6X"},
            
            # Petite Sizes
            {"name": "Petite XS"},
            {"name": "Petite S"},
            {"name": "Petite M"},
            {"name": "Petite L"},
            {"name": "Petite XL"},
            
            # Tall Sizes
            {"name": "Tall S"},
            {"name": "Tall M"},
            {"name": "Tall L"},
            {"name": "Tall XL"},
            {"name": "Tall XXL"},
            
            # Maternity Sizes
            {"name": "Maternity S"},
            {"name": "Maternity M"},
            {"name": "Maternity L"},
            {"name": "Maternity XL"},
            {"name": "Maternity XXL"},
            
            # Big & Tall
            {"name": "Big S"},
            {"name": "Big M"},
            {"name": "Big L"},
            {"name": "Big XL"},
            {"name": "Big XXL"},
            {"name": "Big XXXL"},
            {"name": "Tall Big"},
            
            # Uniform Sizes
            {"name": "Uniform - 34R"},
            {"name": "Uniform - 36R"},
            {"name": "Uniform - 38R"},
            {"name": "Uniform - 40R"},
            {"name": "Uniform - 42R"},
            {"name": "Uniform - 44R"},
            {"name": "Uniform - 34L"},
            {"name": "Uniform - 36L"},
            {"name": "Uniform - 38L"},
            {"name": "Uniform - 40L"},
            {"name": "Uniform - 42L"},
            {"name": "Uniform - 44L"},
            {"name": "Uniform - 34S"},
            {"name": "Uniform - 36S"},
            {"name": "Uniform - 38S"},
            {"name": "Uniform - 40S"},
            {"name": "Uniform - 42S"},
            
            # Sock Sizes
            {"name": "Sock - S"},
            {"name": "Sock - M"},
            {"name": "Sock - L"},
            {"name": "Sock - XL"},
            {"name": "Sock - 4-6"},
            {"name": "Sock - 6-8"},
            {"name": "Sock - 8-10"},
            {"name": "Sock - 10-12"},
            {"name": "Sock - 12-14"},
            
            # Pantyhose/Tights
            {"name": "Tights A"},
            {"name": "Tights B"},
            {"name": "Tights C"},
            {"name": "Tights D"},
            {"name": "Tights E"},
            {"name": "Tights F"},
            
            # Asian Sizes (typically smaller)
            {"name": "Asia XS"},
            {"name": "Asia S"},
            {"name": "Asia M"},
            {"name": "Asia L"},
            {"name": "Asia XL"},
            {"name": "Asia XXL"},
            {"name": "Asia 3XL"},
            
            # European Sizes
            {"name": "EU 32"},
            {"name": "EU 34"},
            {"name": "EU 36"},
            {"name": "EU 38"},
            {"name": "EU 40"},
            {"name": "EU 42"},
            {"name": "EU 44"},
            {"name": "EU 46"},
            {"name": "EU 48"},
            
            # UK Sizes
            {"name": "UK 4"},
            {"name": "UK 6"},
            {"name": "UK 8"},
            {"name": "UK 10"},
            {"name": "UK 12"},
            {"name": "UK 14"},
            {"name": "UK 16"},
            {"name": "UK 18"},
            {"name": "UK 20"},
            {"name": "UK 22"},
            {"name": "UK 24"},
            {"name": "UK 26"},
            {"name": "UK 28"},
            {"name": "UK 30"},
            {"name": "UK 32"},
            
            # US Sizes
            {"name": "US 0"},
            {"name": "US 2"},
            {"name": "US 4"},
            {"name": "US 6"},
            {"name": "US 8"},
            {"name": "US 10"},
            {"name": "US 12"},
            {"name": "US 14"},
            {"name": "US 16"},
            {"name": "US 18"},
            {"name": "US 20"},
            
            # International Size Conversions
            {"name": "Intl XS"},
            {"name": "Intl S"},
            {"name": "Intl M"},
            {"name": "Intl L"},
            {"name": "Intl XL"},
            {"name": "Intl XXL"},
            
            # One Size
            {"name": "One Size"},
            {"name": "OSFA"},  # One Size Fits All
            {"name": "Adjustable"},
            {"name": "Universal"},
            
            # Unisex Sizes
            {"name": "Unisex XS"},
            {"name": "Unisex S"},
            {"name": "Unisex M"},
            {"name": "Unisex L"},
            {"name": "Unisex XL"},
            {"name": "Unisex XXL"},
            
            # Bed Sizes
            {"name": "Twin"},
            {"name": "Twin XL"},
            {"name": "Full"},
            {"name": "Queen"},
            {"name": "King"},
            {"name": "California King"},
            {"name": "Super King"},
            
            # Pillow Sizes
            {"name": "Standard Pillow"},
            {"name": "Queen Pillow"},
            {"name": "King Pillow"},
            {"name": "Body Pillow"},
            {"name": "Neck Pillow"},
            
            # Towel Sizes
            {"name": "Hand Towel"},
            {"name": "Bath Towel"},
            {"name": "Bath Sheet"},
            {"name": "Face Towel"},
            {"name": "Guest Towel"},
            
            # Paper Sizes
            {"name": "A0"},
            {"name": "A1"},
            {"name": "A2"},
            {"name": "A3"},
            {"name": "A4"},
            {"name": "A5"},
            {"name": "A6"},
            {"name": "A7"},
            {"name": "A8"},
            {"name": "Letter"},
            {"name": "Legal"},
            {"name": "Tabloid"},
            
            # Photo Sizes
            {"name": "2x3"},
            {"name": "3x5"},
            {"name": "4x6"},
            {"name": "5x7"},
            {"name": "8x10"},
            {"name": "8.5x11"},
            {"name": "11x14"},
            {"name": "16x20"},
            {"name": "20x24"},
            {"name": "24x36"},
            
            # Frame Sizes
            {"name": "Frame 4x6"},
            {"name": "Frame 5x7"},
            {"name": "Frame 8x10"},
            {"name": "Frame 11x14"},
            {"name": "Frame 16x20"},
            
            # Screen Sizes (inches)
            {"name": '13"'},
            {"name": '14"'},
            {"name": '15"'},
            {"name": '15.6"'},
            {"name": '17"'},
            {"name": '19"'},
            {"name": '21"'},
            {"name": '24"'},
            {"name": '27"'},
            {"name": '32"'},
            {"name": '40"'},
            {"name": '43"'},
            {"name": '50"'},
            {"name": '55"'},
            {"name": '60"'},
            {"name": '65"'},
            {"name": '70"'},
            {"name": '75"'},
            {"name": '82"'},
            {"name": '85"'},
            
            # Luggage Sizes
            {"name": "Carry-on"},
            {"name": "Small Check-in"},
            {"name": "Medium Check-in"},
            {"name": "Large Check-in"},
            {"name": "Extra Large Check-in"},
            
            # Bottle Sizes
            {"name": "50ml"},
            {"name": "100ml"},
            {"name": "200ml"},
            {"name": "250ml"},
            {"name": "500ml"},
            {"name": "750ml"},
            {"name": "1L"},
            {"name": "1.5L"},
            {"name": "2L"},
            {"name": "3L"},
            {"name": "5L"},
            
            # Condiment Sizes
            {"name": "Sachet"},
            {"name": "Mini"},
            {"name": "Regular"},
            {"name": "Family"},
            {"name": "Party"},
            
            # Bangladeshi Local Size Terms
            {"name": "Deshi XS"},
            {"name": "Deshi S"},
            {"name": "Deshi M"},
            {"name": "Deshi L"},
            {"name": "Deshi XL"},
            {"name": "Deshi XXL"},
            {"name": "Panjabi 38"},
            {"name": "Panjabi 40"},
            {"name": "Panjabi 42"},
            {"name": "Panjabi 44"},
            {"name": "Panjabi 46"},
            {"name": "Panjabi 48"},
            {"name": "Panjabi 50"},
            {"name": "Fatua S"},
            {"name": "Fatua M"},
            {"name": "Fatua L"},
            {"name": "Fatua XL"},
            {"name": "Salwar Kameez Small"},
            {"name": "Salwar Kameez Medium"},
            {"name": "Salwar Kameez Large"},
            {"name": "Three Piece Small"},
            {"name": "Three Piece Medium"},
            {"name": "Three Piece Large"},
            {"name": "Kurti S"},
            {"name": "Kurti M"},
            {"name": "Kurti L"},
            {"name": "Kurti XL"},
            
            # Custom/Bespoke
            {"name": "Custom"},
            {"name": "Bespoke"},
            {"name": "Tailored"},
            {"name": "Made to Measure"},
            
            # Numeric Range Sizes
            {"name": "0-2"},
            {"name": "2-4"},
            {"name": "4-6"},
            {"name": "6-8"},
            {"name": "8-10"},
            {"name": "10-12"},
            {"name": "12-14"},
            {"name": "14-16"},
            {"name": "16-18"},
            {"name": "18-20"},
            {"name": "20-22"},
            {"name": "22-24"},
        ]
        
        # Remove duplicates
        seen = set()
        unique_sizes = []
        for size in sizes:
            if size["name"] not in seen:
                seen.add(size["name"])
                unique_sizes.append(size)
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.WARNING(f'Total sizes to process: {len(unique_sizes)}'))
        
        for size_data in unique_sizes:
            try:
                # Create or update size
                obj, created = Size.objects.update_or_create(
                    name=size_data["name"],
                    defaults={}  # No additional fields to update
                )
                
                if created:
                    created_count += 1
                    if created_count <= 10:  # Show first 10 for example
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {size_data["name"]}'))
                else:
                    updated_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {size_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk size creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   └─ Total Sizes: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Sizes: {len(unique_sizes)}\n'
            
            f'\n📋 Size Categories:\n'
            f'   ├─ General Clothing: 10\n'
            f'   ├─ Numeric Clothing: 31\n'
            f'   ├─ Kids Sizes: 19\n'
            f'   ├─ Women\'s Sizes: 11\n'
            f'   ├─ Men\'s Sizes: 9\n'
            f'   ├─ Shoe Sizes (US/UK/EU): ~50\n'
            f'   ├─ Kids/Infant Shoes: 18\n'
            f'   ├─ Jeans Sizes: 23\n'
            f'   ├─ Bra Sizes: 25\n'
            f'   ├─ Ring Sizes: 11\n'
            f'   ├─ Hat Sizes: 17\n'
            f'   ├─ Glove Sizes: 11\n'
            f'   ├─ Belt Sizes: 9\n'
            f'   ├─ Plus/Petite/Tall: 20\n'
            f'   ├─ Uniform Sizes: 18\n'
            f'   ├─ Sock/Tights: 14\n'
            f'   ├─ International Sizes: 30\n'
            f'   ├─ Home (Bed/Towel): 20\n'
            f'   ├─ Paper/Photo/Frame: 30\n'
            f'   ├─ Electronics/Luggage: 25\n'
            f'   ├─ Bottle/Condiment: 15\n'
            f'   ├─ Bangladeshi Local: 27\n'
            f'   ├─ Custom/Bespoke: 4\n'
            f'   └─ Numeric Ranges: 12\n'
        ))