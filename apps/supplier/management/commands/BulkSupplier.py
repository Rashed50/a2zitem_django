import json
import os
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

##? Models Import
from apps.supplier.models import Supplier

"""
##! python manage.py BulkSupplier
"""
class Command(BaseCommand):
    help = 'Bulk supplier creation from predefined data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting bulk supplier creation...'))
        
        suppliers = [
            # Electronics & Gadgets Suppliers
            {
                "name": "Samsung Bangladesh",
                "contact": "Md. Riaz Uddin",
                "email": "info@samsung-bd.com",
                "phone": "+880 2 55678901",
                "address": "Samsung Electronics Bangladesh, Gulshan Avenue, Dhaka 1212"
            },
            {
                "name": "Walton Plaza",
                "contact": "Kamrul Hasan",
                "email": "corporate@waltonbd.com",
                "phone": "+880 2 9887524",
                "address": "Walton Corporate Office, 108 Bir Uttam Mir Shawkat Sarak, Tejgaon, Dhaka 1208"
            },
            {
                "name": "Singer Bangladesh Limited",
                "contact": "Shahidul Islam",
                "email": "info@singerbd.com",
                "phone": "+880 2 8331234",
                "address": "Singer Bhaban, 5/B, Road 18, Gulshan-1, Dhaka 1212"
            },
            {
                "name": "Best Electronics",
                "contact": "Mahbubur Rahman",
                "email": "sales@bestelectronicsbd.com",
                "phone": "+880 2 9638521",
                "address": "44-45, Bangabandhu Road, Chittagong"
            },
            {
                "name": "Ryans Computers",
                "contact": "Tanvir Ahmed",
                "email": "info@ryanscomputers.com",
                "phone": "+880 2 58151234",
                "address": "33 DIL, 7th Floor, Dhaka"
            },
            
            # Garments & Textile Suppliers
            {
                "name": "DBL Group",
                "contact": "M.A. Jabbar",
                "email": "info@dbl-group.com",
                "phone": "+880 2 8854381",
                "address": "DBL Bhaban, Road 8, Sector 1, Uttara, Dhaka 1230"
            },
            {
                "name": "Square Textiles Limited",
                "contact": "Anwar Hossain",
                "email": "info@squaretextiles.com",
                "phone": "+880 2 8835000",
                "address": "Square Centre, 48 Mohakhali C/A, Dhaka 1212"
            },
            {
                "name": "Ha-Meem Group",
                "contact": "Nurul Islam",
                "email": "info@hameemgroup.com",
                "phone": "+880 2 8819460",
                "address": "Ha-Meem Tower, 51 New Eskaton Road, Dhaka 1000"
            },
            {
                "name": "Beximco Textiles",
                "contact": "Salman F Rahman",
                "email": "textiles@beximco.com",
                "phone": "+880 2 58611001",
                "address": "Beximco Industrial Park, Sarabo, Kashimpur, Gazipur"
            },
            {
                "name": "Aarong Supplies",
                "contact": "Taslima Akhter",
                "email": "supplier@aarong.com",
                "phone": "+880 2 58810987",
                "address": "Aarong Head Office, 346 Tejgaon Industrial Area, Dhaka 1208"
            },
            
            # Food & Beverage Suppliers
            {
                "name": "Pran-RFL Group",
                "contact": "Ahsan Khan",
                "email": "procurement@pranrfl.com",
                "phone": "+880 2 48811700",
                "address": "Pran Industrial Park, Bhaluka, Mymensingh"
            },
            {
                "name": "Square Food & Beverage",
                "contact": "Rafiqul Islam",
                "email": "food@squaregroup.com",
                "phone": "+880 2 8833000",
                "address": "Square Centre, 48 Mohakhali C/A, Dhaka 1212"
            },
            {
                "name": "Akij Food & Beverage",
                "contact": "Sheikh Bashir Uddin",
                "email": "info@akijfood.com",
                "phone": "+880 2 48811800",
                "address": "Akij House, 198 Bir Uttam Mir Shawkat Sarak, Tejgaon, Dhaka 1208"
            },
            {
                "name": "Kazi Food Industries",
                "contact": "Kazi Inam Ahmed",
                "email": "info@kazifood.com",
                "phone": "+880 2 9812345",
                "address": "Kazi Tower, 21 Mohakhali C/A, Dhaka 1212"
            },
            {
                "name": "Bombay Sweets & Co.",
                "contact": "Altaf Hossain",
                "email": "orders@bombaysweets.com",
                "phone": "+880 2 7412345",
                "address": "62/1 Purana Paltan, Dhaka 1000"
            },
            
            # Construction & Building Materials
            {
                "name": "Mir Ceramics",
                "contact": "Mirza Salman Ispahani",
                "email": "info@mirceramics.com",
                "phone": "+880 2 9884020",
                "address": "Ispahani Building, 14-15 Motijheel C/A, Dhaka 1000"
            },
            {
                "name": "Rak Ceramics Bangladesh",
                "contact": "Md. Shahid Ullah",
                "email": "bd@rakceramics.com",
                "phone": "+880 2 9812345",
                "address": "Rak Tower, 6-7 Kawran Bazar, Dhaka 1215"
            },
            {
                "name": "Heidelberg Cement Bangladesh",
                "contact": "Mohammad Ali",
                "email": "info@heidelbergbangladesh.com",
                "phone": "+880 2 9885610",
                "address": "Shanta Western Tower, 186 Bir Uttam Mir Shawkat Sarak, Tejgaon, Dhaka 1208"
            },
            
            # Pharmaceutical Suppliers
            {
                "name": "Square Pharmaceuticals Ltd.",
                "contact": "Tapan Chowdhury",
                "email": "supply@squarepharma.com",
                "phone": "+880 2 8833000",
                "address": "Square Centre, 48 Mohakhali C/A, Dhaka 1212"
            },
            {
                "name": "Beximco Pharmaceuticals",
                "contact": "Nazmul Hassan",
                "email": "pharma@beximco.com",
                "phone": "+880 2 58611001",
                "address": "Beximco Industrial Park, Sarabo, Kashimpur, Gazipur"
            },
            {
                "name": "Incepta Pharmaceuticals",
                "contact": "Abdul Muktadir",
                "email": "procurement@inceptapharma.com",
                "phone": "+880 2 8892222",
                "address": "Incepta House, 40 Shahid Tajuddin Ahmed Sarani, Dhaka 1208"
            },
            
            # Furniture Suppliers
            {
                "name": "Hatil Furniture",
                "contact": "Selim H. Rahman",
                "email": "sales@hatil.com",
                "phone": "+880 2 9884151",
                "address": "Hatil Complex, 5-7 North Tejgaon, Dhaka 1208"
            },
            {
                "name": "Otobi Limited",
                "contact": "Dilip Kumar Saha",
                "email": "info@otobi.com",
                "phone": "+880 2 8331191",
                "address": "Otobi Bhaban, 15/1 Topkhana Road, Dhaka 1000"
            },
            {
                "name": "Brothers Furniture",
                "contact": "Hasanuzzaman",
                "email": "info@brothersfurniturebd.com",
                "phone": "+880 2 9666599",
                "address": "150-151 New Elephant Road, Dhaka 1205"
            },
            {
                "name": "Navid Furniture",
                "contact": "Navid Ahmed",
                "email": "sales@navidfurniture.com",
                "phone": "+880 2 9666242",
                "address": "136 New Elephant Road, Dhaka 1205"
            },
            
            # Stationery & Office Supplies
            {
                "name": "Matador Group",
                "contact": "Golam Mostofa",
                "email": "info@matadorgroup.com",
                "phone": "+880 2 9338130",
                "address": "Matador Tower, 50 Kawran Bazar, Dhaka 1215"
            },
            {
                "name": "Helal Stationery",
                "contact": "Helal Uddin",
                "email": "helal@stationerybd.com",
                "phone": "+880 2 7112345",
                "address": "13/1 Bangabandhu Avenue, Dhaka 1000"
            },
            
            # Cosmetic & Personal Care Suppliers
            {
                "name": "Keya Cosmetics",
                "contact": "Abul Khayer",
                "email": "info@keyagroup.com",
                "phone": "+880 2 9884141",
                "address": "Keya Group, 112-113 Motijheel C/A, Dhaka 1000"
            },
            {
                "name": "Kohinoor Chemicals",
                "contact": "Shahidul Alam",
                "email": "info@kohinoorbd.com",
                "phone": "+880 2 9666565",
                "address": "Kohinoor Bhaban, 22 Kazi Nazrul Islam Avenue, Dhaka 1000"
            },
            
            # Logistics & Distribution
            {
                "name": "SA Paribahan",
                "contact": "Shah Alam",
                "email": "dispatch@saparibahan.com",
                "phone": "+880 2 8332090",
                "address": "222/1 Tejgaon Link Road, Dhaka 1208"
            },
            {
                "name": "Continental Traders",
                "contact": "Rafiq Uddin",
                "email": "info@continentaltraders.com",
                "phone": "+880 2 9552875",
                "address": "79 Motijheel C/A, Dhaka 1000"
            },
            
            # International Brands Local Distributors
            {
                "name": "Transcom Electronics",
                "contact": "Taskeen Ahmed",
                "email": "info@transcombd.com",
                "phone": "+880 2 9886688",
                "address": "Transcom Tower, 1/25 North Avenue, Dhaka 1212"
            },
            {
                "name": "Rangs Group",
                "contact": "M. Shamsul Haque",
                "email": "info@rangsbd.com",
                "phone": "+880 2 9886303",
                "address": "Rangs Bhaban, 116/A, Segunbagicha, Dhaka 1000"
            },
            {
                "name": "Global Brand Distributor",
                "contact": "Tanvir Hasan",
                "email": "info@globalbrandbd.com",
                "phone": "+880 2 9854321",
                "address": "SKS Tower, 7 VIP Road, Mohakhali, Dhaka 1206"
            }
        ]
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.WARNING(f'Total suppliers to process: {len(suppliers)}'))
        
        for supplier_data in suppliers:
            try:
                # Create or update supplier
                obj, created = Supplier.objects.update_or_create(
                    name=supplier_data["name"],
                    defaults={
                        "contact": supplier_data.get("contact"),
                        "email": supplier_data.get("email"),
                        "phone": supplier_data.get("phone"),
                        "address": supplier_data.get("address")
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✅ Created: {supplier_data["name"]}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'🔄 Updated: {supplier_data["name"]}'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error creating {supplier_data["name"]}: {str(e)}'))
                skipped_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Bulk supplier creation completed!\n'
            f'📊 Summary:\n'
            f'   ├─ Created: {created_count}\n'
            f'   ├─ Updated: {updated_count}\n'
            f'   ├─ Skipped: {skipped_count}\n'
            f'   └─ Total Suppliers: {created_count + updated_count + skipped_count}\n'
            
            f'\n📋 Supplier Categories:\n'
            f'   ├─ Electronics & Gadgets: 5\n'
            f'   ├─ Garments & Textile: 5\n'
            f'   ├─ Food & Beverage: 5\n'
            f'   ├─ Construction & Materials: 3\n'
            f'   ├─ Pharmaceutical: 3\n'
            f'   ├─ Furniture: 4\n'
            f'   ├─ Stationery & Office: 2\n'
            f'   ├─ Cosmetic & Personal Care: 2\n'
            f'   ├─ Logistics & Distribution: 2\n'
            f'   ├─ International Brands: 3\n'
            f'   └─ Total: 34 Suppliers\n'
        ))