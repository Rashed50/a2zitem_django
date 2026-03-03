import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

##? Models Import
from apps.product.models.color import Color

"""
##TODO:- python manage.py BulkColor
"""
class Command(BaseCommand):
    help = 'Bulk color creation from predefined data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk color creation...'))
        
        colors = [
            # Basic Colors
            {"name": "Red"},
            {"name": "Blue"},
            {"name": "Green"},
            {"name": "Yellow"},
            {"name": "Black"},
            {"name": "White"},
            {"name": "Gray"},
            {"name": "Silver"},
            {"name": "Gold"},
            {"name": "Brown"},
            {"name": "Orange"},
            {"name": "Purple"},
            {"name": "Pink"},
            {"name": "Maroon"},
            {"name": "Navy Blue"},
            {"name": "Sky Blue"},
            {"name": "Light Blue"},
            {"name": "Dark Blue"},
            {"name": "Turquoise"},
            {"name": "Teal"},
            {"name": "Cyan"},
            {"name": "Magenta"},
            {"name": "Lavender"},
            {"name": "Violet"},
            {"name": "Indigo"},
            {"name": "Crimson"},
            {"name": "Scarlet"},
            {"name": "Burgundy"},
            {"name": "Wine Red"},
            {"name": "Rose"},
            {"name": "Coral"},
            {"name": "Salmon"},
            {"name": "Peach"},
            {"name": "Apricot"},
            {"name": "Beige"},
            {"name": "Cream"},
            {"name": "Ivory"},
            {"name": "Off White"},
            {"name": "Tan"},
            {"name": "Khaki"},
            {"name": "Olive"},
            {"name": "Lime"},
            {"name": "Lime Green"},
            {"name": "Mint"},
            {"name": "Mint Green"},
            {"name": "Forest Green"},
            {"name": "Army Green"},
            {"name": "Hunter Green"},
            {"name": "Emerald"},
            {"name": "Jade"},
            {"name": "Sage"},
            {"name": "Sea Green"},
            {"name": "Aqua"},
            {"name": "Aquamarine"},
            
            # Shades of Gray
            {"name": "Charcoal"},
            {"name": "Slate Gray"},
            {"name": "Ash Gray"},
            {"name": "Smoke Gray"},
            {"name": "Steel Gray"},
            {"name": "Iron Gray"},
            {"name": "Pewter"},
            {"name": "Graphite"},
            {"name": "Anthracite"},
            
            # Metallic Colors
            {"name": "Metallic Silver"},
            {"name": "Metallic Gold"},
            {"name": "Rose Gold"},
            {"name": "Bronze"},
            {"name": "Copper"},
            {"name": "Brass"},
            {"name": "Chrome"},
            {"name": "Platinum"},
            {"name": "Titanium"},
            
            # Pastel Colors
            {"name": "Pastel Pink"},
            {"name": "Pastel Blue"},
            {"name": "Pastel Yellow"},
            {"name": "Pastel Green"},
            {"name": "Pastel Purple"},
            {"name": "Pastel Orange"},
            {"name": "Pastel Lavender"},
            {"name": "Pastel Mint"},
            {"name": "Pastel Peach"},
            
            # Neon Colors
            {"name": "Neon Red"},
            {"name": "Neon Blue"},
            {"name": "Neon Green"},
            {"name": "Neon Yellow"},
            {"name": "Neon Orange"},
            {"name": "Neon Pink"},
            {"name": "Neon Purple"},
            {"name": "Electric Blue"},
            {"name": "Electric Green"},
            
            # Skin Tones
            {"name": "Fair"},
            {"name": "Light"},
            {"name": "Medium"},
            {"name": "Tan"},
            {"name": "Olive"},
            {"name": "Brown"},
            {"name": "Dark Brown"},
            {"name": "Ebony"},
            
            # Hair Colors
            {"name": "Blonde"},
            {"name": "Brunette"},
            {"name": "Auburn"},
            {"name": "Chestnut"},
            {"name": "Strawberry Blonde"},
            {"name": "Platinum Blonde"},
            {"name": "Dirty Blonde"},
            {"name": "Honey Blonde"},
            {"name": "Caramel"},
            {"name": "Chocolate Brown"},
            {"name": "Coffee Brown"},
            {"name": "Jet Black"},
            {"name": "Blue Black"},
            {"name": "Silver Gray"},
            {"name": "Salt & Pepper"},
            
            # Eye Colors
            {"name": "Brown Eyes"},
            {"name": "Blue Eyes"},
            {"name": "Green Eyes"},
            {"name": "Hazel Eyes"},
            {"name": "Gray Eyes"},
            {"name": "Amber Eyes"},
            
            # Gemstone Colors
            {"name": "Ruby Red"},
            {"name": "Sapphire Blue"},
            {"name": "Emerald Green"},
            {"name": "Diamond White"},
            {"name": "Amethyst Purple"},
            {"name": "Topaz Yellow"},
            {"name": "Opal"},
            {"name": "Pearl"},
            {"name": "Crystal"},
            
            # Food Colors
            {"name": "Chocolate"},
            {"name": "Coffee"},
            {"name": "Caramel"},
            {"name": "Honey"},
            {"name": "Vanilla"},
            {"name": "Strawberry"},
            {"name": "Cherry"},
            {"name": "Raspberry"},
            {"name": "Blueberry"},
            {"name": "Grape"},
            {"name": "Lemon"},
            {"name": "Lime"},
            {"name": "Orange"},
            {"name": "Peach"},
            {"name": "Mango"},
            {"name": "Pumpkin"},
            {"name": "Cinnamon"},
            {"name": "Nutmeg"},
            
            # Nature Colors
            {"name": "Sky Blue"},
            {"name": "Ocean Blue"},
            {"name": "Sea Foam"},
            {"name": "Sand"},
            {"name": "Desert"},
            {"name": "Earth"},
            {"name": "Moss"},
            {"name": "Fern"},
            {"name": "Pine"},
            {"name": "Birch"},
            {"name": "Maple"},
            {"name": "Oak"},
            {"name": "Walnut"},
            {"name": "Mahogany"},
            {"name": "Rosewood"},
            
            # Flower Colors
            {"name": "Lavender"},
            {"name": "Lilac"},
            {"name": "Orchid"},
            {"name": "Rose Pink"},
            {"name": "Tulip Red"},
            {"name": "Sunflower Yellow"},
            {"name": "Daisy White"},
            {"name": "Lotus Pink"},
            
            # Fabric Colors
            {"name": "Denim Blue"},
            {"name": "Jeans Blue"},
            {"name": "Leather Brown"},
            {"name": "Suede Brown"},
            {"name": "Velvet Red"},
            {"name": "Silk White"},
            {"name": "Cotton White"},
            {"name": "Linen"},
            
            # Print/Pattern Descriptions (sometimes used as colors)
            {"name": "Striped"},
            {"name": "Checked"},
            {"name": "Plaid"},
            {"name": "Floral"},
            {"name": "Polka Dot"},
            {"name": "Geometric"},
            {"name": "Abstract"},
            {"name": "Animal Print"},
            {"name": "Leopard Print"},
            {"name": "Zebra Print"},
            {"name": "Tie Dye"},
            {"name": "Ombre"},
            {"name": "Gradient"},
            
            # Multicolor
            {"name": "Multicolor"},
            {"name": "Rainbow"},
            {"name": "Colorful"},
            {"name": "Mixed Colors"},
            
            # Transparent/Effect
            {"name": "Transparent"},
            {"name": "Clear"},
            {"name": "Translucent"},
            {"name": "Opaque"},
            {"name": "Matte"},
            {"name": "Glossy"},
            {"name": "Shiny"},
            {"name": "Glitter"},
            {"name": "Sparkle"},
            {"name": "Iridescent"},
            {"name": "Holographic"},
            {"name": "Pearlescent"},
            {"name": "Fluorescent"},
            {"name": "Phosphorescent"},
            {"name": "Glow in Dark"},
            
            # Bangladeshi/South Asian Color Names
            {"name": "Shapla White"},  # White water lily
            {"name": "Shada"},  # White (Bengali)
            {"name": "Kalo"},  # Black (Bengali)
            {"name": "Lal"},  # Red (Bengali)
            {"name": "Neel"},  # Blue (Bengali)
            {"name": "Shobuj"},  # Green (Bengali)
            {"name": "Holud"},  # Yellow (Bengali)
            {"name": "Komola"},  # Orange (Bengali)
            {"name": "Beguni"},  # Purple (Bengali)
            {"name": "Golapi"},  # Pink (Bengali)
            {"name": "Badami"},  # Brown (Bengali)
            {"name": "Mosharu"},  # Maroon (Bengali)
            {"name": "Shonali"},  # Golden (Bengali)
            {"name": "Rupali"},  # Silver (Bengali)
            {"name": "Kalo Megh"},  # Dark Cloud
            {"name": "Shada Megh"},  # White Cloud
            {"name": "Shada Golap"},  # White Rose
            {"name": "Lal Golap"},  # Red Rose
            {"name": "Shimul Red"},  # Shimul flower red
            {"name": "Krishnachura Red"},  # Krishnachura flower red
            {"name": "Radhachura Yellow"},  # Radhachura flower yellow
            {"name": "Palash Orange"},  # Palash flower orange
            {"name": "Henna Green"},  # Mehendi green
            {"name": "Jam"},  # Jamun purple
            {"name": "Aam"},  # Mango yellow
            {"name": "Kola"},  # Banana yellow
            {"name": "Lebu"},  # Lemon yellow
            {"name": "Komola Lebu"},  # Orange
            {"name": "Angur"},  # Grape purple
            {"name": "Peyara"},  # Guava green
            {"name": "Shundori"},  # Sundori (beautiful) - a popular saree color
            {"name": "Tangail Saree Red"},  # Traditional Tangail saree red
            {"name": "Jamdani White"},  # Traditional Jamdani white
            {"name": "Muslin White"},  # Traditional Muslin white
            {"name": "Nakshi Kantha Mix"}  # Traditional embroidery mix
        ]
        
        # Remove duplicates
        seen = set()
        unique_colors = []
        for color in colors:
            if color["name"] not in seen:
                seen.add(color["name"])
                unique_colors.append(color)
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.WARNING(f'Total colors to process: {len(unique_colors)}'))
        
        for color_data in unique_colors:
            try:
                # Create or update color
                obj, created = Color.objects.update_or_create(
                    name=color_data["name"],
                    defaults={}  # No additional fields to update
                )
                
                if created:
                    created_count += 1
                    if created_count <= 10:  # Show first 10 for example
                        self.stdout.write(self.style.SUCCESS(f'✅ Created: {color_data["name"]}'))
                else:
                    updated_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {color_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk color creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   └─ Total Colors: {created_count + updated_count + skipped_count}\n'
            f'   └─ Unique Colors: {len(unique_colors)}\n'
            
            f'\n📋 Color Categories:\n'
            f'   ├─ Basic Colors: ~20\n'
            f'   ├─ Shades of Gray: 9\n'
            f'   ├─ Metallic Colors: 9\n'
            f'   ├─ Pastel Colors: 9\n'
            f'   ├─ Neon Colors: 9\n'
            f'   ├─ Skin Tones: 8\n'
            f'   ├─ Hair Colors: 14\n'
            f'   ├─ Eye Colors: 6\n'
            f'   ├─ Gemstone Colors: 9\n'
            f'   ├─ Food Colors: 18\n'
            f'   ├─ Nature Colors: 14\n'
            f'   ├─ Flower Colors: 8\n'
            f'   ├─ Fabric Colors: 8\n'
            f'   ├─ Print/Pattern: 12\n'
            f'   ├─ Multicolor: 4\n'
            f'   ├─ Transparent/Effect: 15\n'
            f'   └─ Bangladeshi Colors: 32\n'
        ))