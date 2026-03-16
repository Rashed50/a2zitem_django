import json
import os
import random
import re
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone

##? Models Import
from apps.product.models.product import Product
from apps.product.models.variant import ProductVariant
from apps.product.models.brand import Brand
from apps.product.models.category import Category
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure

##? Data Import
from .data.productDataSheet import products_data
from .data.productDataSheet import brands_map, categories_map, colors_map, sizes_map, units_map

"""
##TODO:- python manage.py BulkProduct
##TODO:- python manage.py BulkProduct --limit 5
"""
class Command(BaseCommand):
    help = 'Bulk product creation with variants from predefined data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit number of products to process',
            default=None
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate data without creating products',
            default=False
        )
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('🏭 BULK PRODUCT CREATION WITH VARIANTS'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        limit = kwargs.get('limit')
        dry_run = kwargs.get('dry_run')
        
        products_to_process = products_data
        if limit:
            products_to_process = products_data[:limit]
            self.stdout.write(self.style.WARNING(f'📋 Limited to first {limit} products'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No data will be created'))
        
        self.stdout.write(self.style.WARNING(f'\n📦 Total products to process: {len(products_to_process)}'))
        
        # Statistics
        stats = {
            'created_products': 0,
            'updated_products': 0,
            'created_variants': 0,
            'skipped_products': 0,
            'skipped_variants': 0,
            'errors': []
        }
        
        # Validate mappings first
        self.validate_mappings()
        
        # Process each product
        for product_index, product_data in enumerate(products_to_process, 1):
            try:
                self.stdout.write(self.style.WARNING(
                    f'\n[{product_index}/{len(products_to_process)}] 🔄 Processing: {product_data["name"]}'
                ))
                
                if dry_run:
                    self.validate_product_data(product_data)
                    self.stdout.write(self.style.SUCCESS(f'   ✅ Validation passed'))
                    stats['created_products'] += 1
                    stats['created_variants'] += len(product_data['variants'])
                else:
                    with transaction.atomic():
                        product, created, variant_count = self.process_product(product_data)
                        
                        if created:
                            stats['created_products'] += 1
                        else:
                            stats['updated_products'] += 1
                        
                        stats['created_variants'] += variant_count
                        
                        # Show success message
                        status = "✅ CREATED" if created else "🔄 UPDATED"
                        self.stdout.write(self.style.SUCCESS(
                            f'   {status}: {product.name} (Code: {product.code})'
                        ))
                        self.stdout.write(self.style.SUCCESS(
                            f'   └─ Variants: {variant_count}'
                        ))
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ❌ ERROR: {str(e)}'))
                stats['skipped_products'] += 1
                stats['errors'].append(f"{product_data['name']}: {str(e)}")
        
        # Final summary
        self.print_summary(stats, dry_run)
    
    def validate_mappings(self):
        """Validate all mappings have corresponding database records"""
        self.stdout.write(self.style.WARNING('\n🔍 Validating mappings...'))
        
        # Check brands
        missing_brands = []
        for brand_name, brand_id in brands_map.items():
            if not Brand.objects.filter(id=brand_id).exists():
                missing_brands.append(f"{brand_name} (ID: {brand_id})")
        
        if missing_brands:
            self.stdout.write(self.style.ERROR(f'   ❌ Missing brands: {", ".join(missing_brands)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ All {len(brands_map)} brands found'))
        
        # Check categories
        missing_categories = []
        for cat_name, cat_id in categories_map.items():
            if not Category.objects.filter(id=cat_id).exists():
                missing_categories.append(f"{cat_name} (ID: {cat_id})")
        
        if missing_categories:
            self.stdout.write(self.style.ERROR(f'   ❌ Missing categories: {", ".join(missing_categories)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ All {len(categories_map)} categories found'))
        
        # Check colors
        missing_colors = []
        for color_name, color_id in colors_map.items():
            if not Color.objects.filter(id=color_id).exists():
                missing_colors.append(f"{color_name} (ID: {color_id})")
        
        if missing_colors:
            self.stdout.write(self.style.ERROR(f'   ❌ Missing colors: {", ".join(missing_colors)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ All {len(colors_map)} colors found'))
        
        # Check sizes
        missing_sizes = []
        for size_name, size_id in sizes_map.items():
            if not Size.objects.filter(id=size_id).exists():
                missing_sizes.append(f"{size_name} (ID: {size_id})")
        
        if missing_sizes:
            self.stdout.write(self.style.ERROR(f'   ❌ Missing sizes: {", ".join(missing_sizes)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ All {len(sizes_map)} sizes found'))
        
        # Check units
        missing_units = []
        for unit_name, unit_id in units_map.items():
            if not UnitOfMeasure.objects.filter(id=unit_id).exists():
                missing_units.append(f"{unit_name} (ID: {unit_id})")
        
        if missing_units:
            self.stdout.write(self.style.ERROR(f'   ❌ Missing units: {", ".join(missing_units)}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ All {len(units_map)} units found'))
        
        if any([missing_brands, missing_categories, missing_colors, missing_sizes, missing_units]):
            raise Exception("Mapping validation failed. Please fix missing records.")
    
    def validate_product_data(self, product_data):
        """Validate product data without creating"""
        required_fields = ['name', 'title', 'brand_name', 'category_name', 'variants']
        for field in required_fields:
            if field not in product_data:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(product_data['variants'], list):
            raise ValueError("Variants must be a list")
        
        if len(product_data['variants']) == 0:
            raise ValueError("Product must have at least one variant")
    
    def process_product(self, product_data):
        """
        Process a single product and its variants
        Returns: (product, created_flag, variant_count)
        """
        # Get brand
        brand_id = brands_map.get(product_data["brand_name"])
        if not brand_id:
            raise ValueError(f"Brand '{product_data['brand_name']}' not found in mapping")
        brand = Brand.objects.get(id=brand_id)
        
        # Get category
        category_id = categories_map.get(product_data["category_name"])
        if not category_id:
            raise ValueError(f"Category '{product_data['category_name']}' not found in mapping")
        category = Category.objects.get(id=category_id)
        
        # Prepare product data
        product_defaults = {
            "title": product_data["title"],
            "brand": brand,
            "category": category,
            "description": product_data.get("description", ""),
            "is_featured": product_data.get("is_featured", False),
            "is_active": product_data.get("is_active", True),
            "metadata": product_data.get("metadata", {}),
        }
        
        # Create or update product
        product, created = Product.objects.update_or_create(
            name=product_data["name"],
            defaults=product_defaults
        )
        
        # Process variants
        variant_count = 0
        for variant_data in product_data["variants"]:
            try:
                self.process_variant(product, variant_data)
                variant_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'      ⚠️ Variant error ({variant_data.get("color_name", "N/A")}): {str(e)}'
                ))
                stats['skipped_variants'] += 1
        
        return product, created, variant_count
    
    def process_variant(self, product, variant_data):
        """
        Process a single product variant
        """
        # Get color
        color_id = colors_map.get(variant_data["color_name"])
        if not color_id:
            raise ValueError(f"Color '{variant_data['color_name']}' not found in mapping")
        color = Color.objects.get(id=color_id)
        
        # Get size
        size_id = sizes_map.get(variant_data["size_name"])
        if not size_id:
            raise ValueError(f"Size '{variant_data['size_name']}' not found in mapping")
        size = Size.objects.get(id=size_id)
        
        # Get unit
        unit_id = units_map.get(variant_data["unit_name"])
        if not unit_id:
            raise ValueError(f"Unit '{variant_data['unit_name']}' not found in mapping")
        unit = UnitOfMeasure.objects.get(id=unit_id)
        
        # Check if variant exists with same color and size
        existing_variant = ProductVariant.objects.filter(
            product=product,
            color=color,
            size=size
        ).first()
        
        variant_defaults = {
            "stock": variant_data["stock"],
            "min_stock": variant_data.get("min_stock", 0),
            "unit": unit,
            "selling_price": variant_data["selling_price"],
            "purchase_price": variant_data.get("purchase_price", "0.00"),
            "is_default": variant_data.get("is_default", False)
        }
        
        if existing_variant:
            # Update existing variant
            for key, value in variant_defaults.items():
                setattr(existing_variant, key, value)
            existing_variant.save()
            return existing_variant
        else:
            # Create new variant
            variant = ProductVariant.objects.create(
                product=product,
                color=color,
                size=size,
                **variant_defaults
            )
            return variant
    
    def print_summary(self, stats, dry_run):
        """Print final summary"""
        mode = "DRY RUN" if dry_run else "LIVE"
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS(f'🏁 BULK PRODUCT CREATION COMPLETED [{mode}]'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        self.stdout.write(self.style.SUCCESS(f'''
📊 FINAL SUMMARY:
   ├─ Products Created : {stats['created_products']}
   ├─ Products Updated : {stats['updated_products']}
   ├─ Products Skipped : {stats['skipped_products']}
   ├─ Variants Created : {stats['created_variants']}
   └─ Variants Skipped : {stats.get('skipped_variants', 0)}

📈 DATABASE STATUS:
   ├─ Total Products : {Product.objects.count()}
   └─ Total Variants : {ProductVariant.objects.count()}
        '''))
        
        if stats['errors']:
            self.stdout.write(self.style.WARNING('\n⚠️ ERRORS:'))
            for error in stats['errors'][:5]:
                self.stdout.write(self.style.WARNING(f'   • {error}'))
            if len(stats['errors']) > 5:
                self.stdout.write(self.style.WARNING(f'   • ... and {len(stats["errors"]) - 5} more errors'))