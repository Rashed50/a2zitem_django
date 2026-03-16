products_data = [
    ### Smartphones (category: Smartphones)
    {
        "name"          : "iPhone 16 Pro Max",
        "title"         : "Apple iPhone 16 Pro Max - 512GB, Titanium Gray",
        "brand_name"    : "Apple",
        "category_name" : "Smartphones",
        "is_active"     : True,
        "is_featured"   : True,
        "description" : "6.9-inch Super Retina XDR display | A18 Pro chip | 48MP main camera | 5x optical zoom | Titanium design | USB-C 3.0 | 4676mAh battery",
        "variants": [
            {"color_name": "Black", "size_name": "512GB", "unit_name": "Piece", "stock": 15, "selling_price": "149999.00"},
            {"color_name": "White", "size_name": "512GB", "unit_name": "Piece", "stock": 10, "selling_price": "149999.00"},
            {"color_name": "Blue",  "size_name": "1TB", "unit_name": "Piece", "stock": 8, "selling_price": "169999.00"}
        ]
    },
    {
        "name": "Google Pixel 9 Pro XL",
        "title": "Google Pixel 9 Pro XL - 256GB, Obsidian",
        "description": "6.8-inch LTPO OLED | Google Tensor G4 chip | 50MP main + 48MP ultrawide + 48MP telephoto | 7 years of OS updates | 5050mAh battery",
        "brand_name": "Google",
        "category_name": "Smartphones",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Black", "size_name": "256GB", "unit_name": "Piece", "stock": 12, "selling_price": "119999.00"},
            {"color_name": "White", "size_name": "256GB", "unit_name": "Piece", "stock": 8, "selling_price": "119999.00"},
            {"color_name": "Coral", "size_name": "512GB", "unit_name": "Piece", "stock": 5, "selling_price": "139999.00"}
        ]
    },
    {
        "name": "OnePlus 13",
        "title": "OnePlus 13 - 256GB, Emerald Green",
        "description": "6.82-inch LTPO AMOLED | Snapdragon 8 Gen 4 | 50MP triple camera with Hasselblad | 100W fast charging | 5000mAh battery | IP68 rating",
        "brand_name": "OnePlus",
        "category_name": "Smartphones",
        "is_active": True,
        "is_featured": False,
        "variants": [
            {"color_name": "Green", "size_name": "256GB", "unit_name": "Piece", "stock": 20, "selling_price": "89999.00"},
            {"color_name": "Black", "size_name": "256GB", "unit_name": "Piece", "stock": 15, "selling_price": "89999.00"},
            {"color_name": "White", "size_name": "512GB", "unit_name": "Piece", "stock": 10, "selling_price": "99999.00"}
        ]
    },
    {
        "name": "Xiaomi 14 Ultra",
        "title": "Xiaomi 14 Ultra - 512GB, Black",
        "description": "6.73-inch LTPO AMOLED | Snapdragon 8 Gen 3 | 50MP quad camera with Leica | 90W wired + 50W wireless | 5300mAh battery",
        "brand_name": "Xiaomi",
        "category_name": "Smartphones",
        "is_active": True,
        "is_featured": False,
        "variants": [
            {"color_name": "Black", "size_name": "512GB", "unit_name": "Piece", "stock": 18, "selling_price": "109999.00"},
            {"color_name": "White", "size_name": "512GB", "unit_name": "Piece", "stock": 12, "selling_price": "109999.00"},
            {"color_name": "Blue", "size_name": "1TB", "unit_name": "Piece", "stock": 7, "selling_price": "129999.00"}
        ]
    },
    
    ### Laptops (category: Laptops)
    {
        "name": "MacBook Pro 16 M4",
        "title": "Apple MacBook Pro 16 - M4 Max, 1TB SSD",
        "description": "16.2-inch Liquid Retina XDR display | Apple M4 Max chip with 16-core CPU | 40-core GPU | 1TB SSD | 48GB RAM | 22-hour battery life",
        "brand_name": "Apple",
        "category_name": "Laptops",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Silver", "size_name": "1TB", "unit_name": "Piece", "stock": 8, "selling_price": "249999.00"},
            {"color_name": "Space Gray", "size_name": "2TB", "unit_name": "Piece", "stock": 5, "selling_price": "289999.00"},
            {"color_name": "Black", "size_name": "4TB", "unit_name": "Piece", "stock": 3, "selling_price": "329999.00"}
        ]
    },
    {
        "name": "Dell XPS 16",
        "title": "Dell XPS 16 - Intel Core Ultra 9, 32GB RAM",
        "description": "16.3-inch 4K OLED InfinityEdge display | Intel Core Ultra 9 185H | NVIDIA RTX 4070 | 32GB LPDDR5x | 1TB SSD | Windows 11 Pro",
        "brand_name": "Dell",
        "category_name": "Laptops",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Silver", "size_name": "1TB", "unit_name": "Piece", "stock": 10, "selling_price": "189999.00"},
            {"color_name": "Black", "size_name": "2TB", "unit_name": "Piece", "stock": 7, "selling_price": "219999.00"}
        ]
    },
    {
        "name": "ASUS ROG Zephyrus G16",
        "title": "ASUS ROG Zephyrus G16 - Gaming Laptop",
        "description": "16-inch QHD+ 240Hz display | Intel Core i9-14900H | NVIDIA RTX 4090 | 32GB DDR5 | 2TB SSD | RGB keyboard | Windows 11",
        "brand_name": "Asus",
        "category_name": "Laptops",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Gray", "size_name": "2TB", "unit_name": "Piece", "stock": 6, "selling_price": "279999.00"},
            {"color_name": "White", "size_name": "2TB", "unit_name": "Piece", "stock": 4, "selling_price": "279999.00"}
        ]
    },
    
    ### Tablets (category: Tablets)
    {
        "name": "iPad Pro 13 M4",
        "title": "Apple iPad Pro 13 - M4 chip, 512GB",
        "description": "13-inch Ultra Retina XDR display | Apple M4 chip | 12MP front camera with Center Stage | 5G support | Thunderbolt 4 | Magic Keyboard compatible",
        "brand_name": "Apple",
        "category_name": "Tablets",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Silver", "size_name": "512GB", "unit_name": "Piece", "stock": 12, "selling_price": "149999.00"},
            {"color_name": "Space Gray", "size_name": "1TB", "unit_name": "Piece", "stock": 8, "selling_price": "179999.00"},
            {"color_name": "Blue", "size_name": "2TB", "unit_name": "Piece", "stock": 5, "selling_price": "209999.00"}
        ]
    },
    {
        "name": "Samsung Galaxy Tab S10 Ultra",
        "title": "Samsung Galaxy Tab S10 Ultra - 512GB, 5G",
        "description": "14.6-inch Dynamic AMOLED 2X 120Hz | MediaTek Dimensity 9300+ | 14MP + 12MP dual rear camera | S Pen included | 11200mAh battery",
        "brand_name": "Samsung",
        "category_name": "Tablets",
        "is_active": True,
        "is_featured": False,
        "variants": [
            {"color_name": "Gray", "size_name": "512GB", "unit_name": "Piece", "stock": 9, "selling_price": "129999.00"},
            {"color_name": "Beige", "size_name": "1TB", "unit_name": "Piece", "stock": 6, "selling_price": "149999.00"}
        ]
    },
    
    ### Smart Watches (category: Smart Watches)
    {
        "name": "Apple Watch Ultra 3",
        "title": "Apple Watch Ultra 3 - 49mm Titanium",
        "description": "49mm titanium case | Always-on Retina display | Dual-frequency GPS | Depth gauge + water temperature sensor | Siren | 36-hour battery life",
        "brand_name": "Apple",
        "category_name": "Smart Watches",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Black", "size_name": "49mm", "unit_name": "Piece", "stock": 15, "selling_price": "89999.00"},
            {"color_name": "Silver", "size_name": "49mm", "unit_name": "Piece", "stock": 12, "selling_price": "89999.00"},
            {"color_name": "Blue", "size_name": "49mm", "unit_name": "Piece", "stock": 8, "selling_price": "89999.00"}
        ]
    },
    {
        "name": "Samsung Galaxy Watch7 Ultra",
        "title": "Samsung Galaxy Watch7 Ultra - LTE",
        "description": "47mm titanium case | 3nm Exynos processor | BioActive sensor | Blood pressure monitoring | ECG | 590mAh battery | IP68/MIL-STD-810H",
        "brand_name": "Samsung",
        "category_name": "Smart Watches",
        "is_active": True,
        "is_featured": False,
        "variants": [
            {"color_name": "Black", "size_name": "47mm", "unit_name": "Piece", "stock": 18, "selling_price": "59999.00"},
            {"color_name": "Silver", "size_name": "47mm", "unit_name": "Piece", "stock": 14, "selling_price": "59999.00"},
            {"color_name": "Gold", "size_name": "47mm", "unit_name": "Piece", "stock": 10, "selling_price": "64999.00"}
        ]
    },
    
    ### Headphones (category: Headphones)
    {
        "name": "Sony WH-1000XM6",
        "title": "Sony WH-1000XM6 - Wireless Noise Cancelling",
        "description": "Industry-leading noise cancellation | 40-hour battery life with ANC | LDAC support | 360 Reality Audio | Multipoint connection | Foldable design",
        "brand_name": "Sony",
        "category_name": "Headphones",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Black", "size_name": "Standard", "unit_name": "Piece", "stock": 25, "selling_price": "39999.00"},
            {"color_name": "Silver", "size_name": "Standard", "unit_name": "Piece", "stock": 20, "selling_price": "39999.00"},
            {"color_name": "Blue", "size_name": "Standard", "unit_name": "Piece", "stock": 15, "selling_price": "39999.00"}
        ]
    },
    {
        "name": "Bose QuietComfort Ultra",
        "title": "Bose QuietComfort Ultra - Wireless Headphones",
        "description": "CustomTune sound calibration | Immersive Audio | 24-hour battery life | Bluetooth 5.3 | Fold-flat design | World-class noise cancellation",
        "brand_name": "Bose",
        "category_name": "Headphones",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Black", "size_name": "Standard", "unit_name": "Piece", "stock": 18, "selling_price": "44999.00"},
            {"color_name": "White", "size_name": "Standard", "unit_name": "Piece", "stock": 12, "selling_price": "44999.00"}
        ]
    },
    
    ### Fashion - Men's Shoes (category: Shoes)
    {
        "name": "Nike Air Max Pulse",
        "title": "Nike Air Max Pulse - Men's Running Shoes",
        "description": "Breathable mesh upper | Air Max cushioning | Rubber outsole | Reflective details | Multiple colorways | Perfect for running and casual wear",
        "brand_name": "Nike",
        "category_name": "Shoes",
        "is_active": True,
        "is_featured": False,
        "variants": [
            {"color_name": "Black", "size_name": "42", "unit_name": "Pair", "stock": 30, "selling_price": "12999.00"},
            {"color_name": "Black", "size_name": "43", "unit_name": "Pair", "stock": 28, "selling_price": "12999.00"},
            {"color_name": "Black", "size_name": "44", "unit_name": "Pair", "stock": 25, "selling_price": "12999.00"},
            {"color_name": "White", "size_name": "42", "unit_name": "Pair", "stock": 22, "selling_price": "12999.00"},
            {"color_name": "White", "size_name": "43", "unit_name": "Pair", "stock": 20, "selling_price": "12999.00"}
        ]
    },
    {
        "name": "Adidas Ultraboost 23",
        "title": "Adidas Ultraboost 23 - Men's Running Shoes",
        "description": "Adidas Primeknit upper | Boost midsole | Torsion system | Continental rubber outsole | Energy-returning cushioning",
        "brand_name": "Adidas",
        "category_name": "Shoes",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Black", "size_name": "42", "unit_name": "Pair", "stock": 25, "selling_price": "15999.00"},
            {"color_name": "Black", "size_name": "43", "unit_name": "Pair", "stock": 23, "selling_price": "15999.00"},
            {"color_name": "Black", "size_name": "44", "unit_name": "Pair", "stock": 20, "selling_price": "15999.00"},
            {"color_name": "Blue", "size_name": "42", "unit_name": "Pair", "stock": 15, "selling_price": "15999.00"},
            {"color_name": "Blue", "size_name": "43", "unit_name": "Pair", "stock": 14, "selling_price": "15999.00"}
        ]
    },
    
    ### Fashion - Men's Shirts (category: Shirts)
    {
        "name": "Oxford Casual Shirt",
        "title": "Oxford Casual Cotton Shirt - Blue Check",
        "description": "100% premium cotton | Regular fit | Button-down collar | Chest pocket | Machine washable | Perfect for office and casual wear",
        "brand_name": "Levi's",
        "category_name": "Shirts",
        "is_active": True,
        "is_featured": False,
        "variants": [
            {"color_name": "Blue", "size_name": "M", "unit_name": "Piece", "stock": 50, "selling_price": "3499.00"},
            {"color_name": "Blue", "size_name": "L", "unit_name": "Piece", "stock": 45, "selling_price": "3499.00"},
            {"color_name": "Blue", "size_name": "XL", "unit_name": "Piece", "stock": 40, "selling_price": "3499.00"},
            {"color_name": "Red", "size_name": "M", "unit_name": "Piece", "stock": 35, "selling_price": "3499.00"},
            {"color_name": "Red", "size_name": "L", "unit_name": "Piece", "stock": 32, "selling_price": "3499.00"}
        ]
    },
    
    ### Home & Living - Furniture (category: Sofas)
    {
        "name": "Sectional Sofa Set",
        "title": "Modern L-Shaped Sectional Sofa - Gray",
        "description": "Fabric upholstery | L-shaped design | Removable covers | Foam filling | Solid wood frame | Seats up to 6 people | Easy assembly",
        "brand_name": "IKEA",
        "category_name": "Sofas",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Gray", "size_name": "3-Seater", "unit_name": "Piece", "stock": 8, "selling_price": "45999.00"},
            {"color_name": "Beige", "size_name": "3-Seater", "unit_name": "Piece", "stock": 6, "selling_price": "45999.00"},
            {"color_name": "Blue", "size_name": "4-Seater", "unit_name": "Piece", "stock": 5, "selling_price": "55999.00"}
        ]
    },
    
    ### Sports - Cricket (category: Cricket Bats)
    {
        "name": "English Willow Cricket Bat",
        "title": "Grade 1 English Willow Cricket Bat - Short Handle",
        "description": "Grade 1 English willow | Short handle | Sweet spot | Toe protection | Cane handle with rubber grip | Lightweight | For professional players",
        "brand_name": "Apex",
        "category_name": "Cricket Bats",
        "is_active": True,
        "is_featured": True,
        "variants": [
            {"color_name": "Green", "size_name": "Short Handle", "unit_name": "Piece", "stock": 12, "selling_price": "12999.00"},
            {"color_name": "Green", "size_name": "Long Handle", "unit_name": "Piece", "stock": 8, "selling_price": "13999.00"}
        ]
    }
]


# Brands mapping
brands_map = {
    "Apple"   : 1,          
    "Samsung" : 2,        
    "Google"  : 5,         
    "OnePlus" : 4,        
    "Xiaomi"  : 3,         
    "Dell"    : 12,           
    "Asus"    : 13,           
    "Sony"    : 6,           
    "Bose"    : 27,          
    "Nike"    : 42,          
    "Adidas"  : 43,        
    "Levi's"  : 47,        
    "IKEA"    : 134,          
    "Apex"    : 184          
}

# Categories mapping
categories_map = {
    "Smartphones"   : 9,    
    "Laptops"       : 12,       
    "Tablets"       : 13,       
    "Smart Watches" : 14, 
    "Headphones"    : 15,    
    "Shoes"         : 22,         
    "Shirts"        : 20,        
    "Sofas"         : 31,         
    "Cricket Bats"  : 49   
}

# Colors mapping
colors_map = {
    "Black"      : 5,
    "White"      : 6,
    "Silver"     : 8,
    "Space Gray" : 113,
    "Gray"       : 7,
    "Blue"       : 2,
    "Green"      : 3,
    "Red"        : 1,
    "Gold"       : 9,
    "Beige"      : 35,
    "Coral"      : 31,
    "Green"      : 3
}

# Sizes mapping
sizes_map = {
    "512GB": 492,
    "1TB": 493,
    "2TB": 494,
    "4TB": 495,
    "256GB": 491,
    "49mm": 609,
    "38mm": 602,
    "Standard": 483,
    "42": 32,
    "43": 409,
    "44": 33,
    "M": 4,
    "L": 5,
    "XL": 6,
    "3-Seater": 666,
    "4-Seater": 667,
    "Short Handle": 681,
    "Long Handle":682 
}

# Units mapping
units_map = {
    "Piece": 29,
    "Pair": 30
}

