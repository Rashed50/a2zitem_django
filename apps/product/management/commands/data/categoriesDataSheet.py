categories_data = [
    ##! ============================================
    ##!              Main Categories (IDs: 1-5)
    ##! ============================================
    {
        "name": "Electronics",
        "parent": None,
        "preferred_id": 1
    },
    {
        "name": "Fashion",
        "parent": None,
        "preferred_id": 2
    },
    {
        "name": "Home & Living",
        "parent": None,
        "preferred_id": 3
    },
    {
        "name": "Books & Education",
        "parent": None,
        "preferred_id": 4
    },
    {
        "name": "Sports",
        "parent": None,
        "preferred_id": 5
    },
    
    ##! ============================================
    ##!              Electronics Subcategories
    ##! ============================================
    
    ##? Electronics Level 1 (IDs: 6-8)
    {
        "name": "Mobile Phones",
        "parent": "Electronics",
        "preferred_id": 6
    },
    {
        "name": "Computers",
        "parent": "Electronics",
        "preferred_id": 7
    },
    {
        "name": "Gadgets",
        "parent": "Electronics",
        "preferred_id": 8
    },
    
    ##? Mobile Phone Level 2 (IDs: 9-10)
    {
        "name": "Smartphones",
        "parent": "Mobile Phones",
        "preferred_id": 9
    },
    {
        "name": "Feature Phones",
        "parent": "Mobile Phones",
        "preferred_id": 10
    },
    
    ##? Computers Level 2 (IDs: 11-13)
    {
        "name": "Desktops",
        "parent": "Computers",
        "preferred_id": 11
    },
    {
        "name": "Laptops",
        "parent": "Computers",
        "preferred_id": 12
    },
    {
        "name": "Tablets",
        "parent": "Computers",
        "preferred_id": 13
    },
    
    ##? Gadgets Level 2 (IDs: 14-16)
    {
        "name": "Smart Watches",
        "parent": "Gadgets",
        "preferred_id": 14
    },
    {
        "name": "Headphones",
        "parent": "Gadgets",
        "preferred_id": 15
    },
    {
        "name": "Power Banks",
        "parent": "Gadgets",
        "preferred_id": 16
    },
    
    ##! ============================================
    ##!              Fashion Subcategories
    ##! ============================================
    
    ##? Fashion Level 1 (IDs: 17-19)
    {
        "name": "Men's Fashion",
        "parent": "Fashion",
        "preferred_id": 17
    },
    {
        "name": "Women's Fashion",
        "parent": "Fashion",
        "preferred_id": 18
    },
    {
        "name": "Kids' Fashion",
        "parent": "Fashion",
        "preferred_id": 19
    },
    
    ##? Men's Fashion Level 2 (IDs: 20-22)
    {
        "name": "Shirts",
        "parent": "Men's Fashion",
        "preferred_id": 20
    },
    {
        "name": "Pants",
        "parent": "Men's Fashion",
        "preferred_id": 21
    },
    {
        "name": "Shoes",
        "parent": "Men's Fashion",
        "preferred_id": 22
    },
    
    ##? Women's Fashion Level 2 (IDs: 23-25)
    {
        "name": "Saris",
        "parent": "Women's Fashion",
        "preferred_id": 23
    },
    {
        "name": "Three-piece",
        "parent": "Women's Fashion",
        "preferred_id": 24
    },
    {
        "name": "Women's Shoes",
        "parent": "Women's Fashion",
        "preferred_id": 25
    },
    
    ##? Kids' Fashion Level 2 (IDs: 26-27)
    {
        "name": "Baby Dresses",
        "parent": "Kids' Fashion",
        "preferred_id": 26
    },
    {
        "name": "School Uniforms",
        "parent": "Kids' Fashion",
        "preferred_id": 27
    },
    
    ##! ============================================
    ##!              Home & Living Subcategories
    ##! ============================================
    
    ##? Home & Living Level 1 (IDs: 28-30)
    {
        "name": "Furniture",
        "parent": "Home & Living",
        "preferred_id": 28
    },
    {
        "name": "Kitchen",
        "parent": "Home & Living",
        "preferred_id": 29
    },
    {
        "name": "Decor",
        "parent": "Home & Living",
        "preferred_id": 30
    },
    
    ##? Furniture Level 2 (IDs: 31-33)
    {
        "name": "Sofas",
        "parent": "Furniture",
        "preferred_id": 31
    },
    {
        "name": "Dining Tables",
        "parent": "Furniture",
        "preferred_id": 32
    },
    {
        "name": "Beds",
        "parent": "Furniture",
        "preferred_id": 33
    },
    
    ##? Kitchen Level 2 (IDs: 34-35)
    {
        "name": "Cookware",
        "parent": "Kitchen",
        "preferred_id": 34
    },
    {
        "name": "Dinner Sets",
        "parent": "Kitchen",
        "preferred_id": 35
    },
    
    ##? Decor Level 2 (IDs: 36-37)
    {
        "name": "Wall Art",
        "parent": "Decor",
        "preferred_id": 36
    },
    {
        "name": "Vases",
        "parent": "Decor",
        "preferred_id": 37
    },
    
    ##! ============================================
    ##!         Books & Education Subcategories
    ##! ============================================
    
    ##? Books & Education Level 1 (IDs: 38-39)
    {
        "name": "Academic Books",
        "parent": "Books & Education",  # This was causing error? Let's check
        "preferred_id": 38
    },
    {
        "name": "Story Books",
        "parent": "Books & Education",
        "preferred_id": 39
    },
    
    ##? Academic Books Level 2 (IDs: 40-42)
    {
        "name": "Science Books",
        "parent": "Academic Books",
        "preferred_id": 40
    },
    {
        "name": "Math Books",
        "parent": "Academic Books",
        "preferred_id": 41
    },
    {
        "name": "English Books",
        "parent": "Academic Books",
        "preferred_id": 42
    },
    
    ##? Story Books Level 2 (IDs: 43-45)
    {
        "name": "Novels",
        "parent": "Story Books",
        "preferred_id": 43
    },
    {
        "name": "Short Stories",
        "parent": "Story Books",
        "preferred_id": 44
    },
    {
        "name": "Comics",
        "parent": "Story Books",
        "preferred_id": 45
    },
    
    ##! ============================================
    ##!              Sports Subcategories
    ##! ============================================
    
    ##? Sports Level 1 (IDs: 46-48)
    {
        "name": "Cricket",
        "parent": "Sports",
        "preferred_id": 46
    },
    {
        "name": "Football",
        "parent": "Sports",
        "preferred_id": 47
    },
    {
        "name": "Badminton",
        "parent": "Sports",
        "preferred_id": 48
    },
    
    ##? Cricket Level 2 (IDs: 49-51)
    {
        "name": "Cricket Bats",
        "parent": "Cricket",
        "preferred_id": 49
    },
    {
        "name": "Cricket Balls",
        "parent": "Cricket",
        "preferred_id": 50
    },
    {
        "name": "Cricket Pads",
        "parent": "Cricket",
        "preferred_id": 51
    },
    
    ##? Football Level 2 (IDs: 52-54)
    {
        "name": "Football Balls",
        "parent": "Football",
        "preferred_id": 52
    },
    {
        "name": "Football Jerseys",
        "parent": "Football",
        "preferred_id": 53
    },
    {
        "name": "Football Boots",
        "parent": "Football",
        "preferred_id": 54
    },
    
    ##? Badminton Level 2 (IDs: 55-56)
    {
        "name": "Badminton Rackets",
        "parent": "Badminton",
        "preferred_id": 55
    },
    {
        "name": "Shuttlecocks",
        "parent": "Badminton",
        "preferred_id": 56
    }
]