# currencies/constants.py
from django.db import models
from django.utils.translation import gettext_lazy as _
# import pytz
# import pycountry

class UserChoices:
    class BloodGroupChoices(models.TextChoices):
        A_POSITIVE  = 'A+', _('A+')
        A_NEGATIVE  = 'A-', _('A-')
        B_POSITIVE  = 'B+', _('B+')
        B_NEGATIVE  = 'B-', _('B-')
        AB_POSITIVE = 'AB+', _('AB+')
        AB_NEGATIVE = 'AB-', _('AB-')
        O_POSITIVE  = 'O+', _('O+')
        O_NEGATIVE  = 'O-', _('O-')
        

class BangladeshConstants:
    """Bangladesh-based constants for company setup"""
    
    # ====================
    # CURRENCIES
    # ====================
    class CurrencyChoices(models.TextChoices):
        BDT = 'BDT', _('Bangladeshi Taka (৳)')
        # USD = 'USD', _('US Dollar ($)')
        # EUR = 'EUR', _('Euro (€)')
        # GBP = 'GBP', _('British Pound (£)')
        # INR = 'INR', _('Indian Rupee (₹)')
        # SAR = 'SAR', _('Saudi Riyal (ر.س)')
        # AED = 'AED', _('UAE Dirham (د.إ)')
        # CNY = 'CNY', _('Chinese Yuan (¥)')
        # JPY = 'JPY', _('Japanese Yen (¥)')
    
    # ====================
    # TIMEZONES
    # ====================
    # Bangladesh timezone and related timezones
    class TimezoneChoices(models.TextChoices):
        ASIA_DHAKA = 'Asia/Dhaka', _('Bangladesh (Dhaka) - GMT+6')
        # ASIA_KOLKATA = 'Asia/Kolkata', _('India (Kolkata) - GMT+5:30')
        # ASIA_KATHMANDU = 'Asia/Kathmandu', _('Nepal (Kathmandu) - GMT+5:45')
        # ASIA_YANGON = 'Asia/Yangon', _('Myanmar (Yangon) - GMT+6:30')
        # ASIA_BANGKOK = 'Asia/Bangkok', _('Thailand (Bangkok) - GMT+7')
        # ASIA_SINGAPORE = 'Asia/Singapore', _('Singapore - GMT+8')
        # ASIA_DUBAI = 'Asia/Dubai', _('UAE (Dubai) - GMT+4')
        # ASIA_RIYADH = 'Asia/Riyadh', _('Saudi Arabia (Riyadh) - GMT+3')
        # ASIA_KARACHI = 'Asia/Karachi', _('Pakistan (Karachi) - GMT+5')
        # ASIA_COLOMBO = 'Asia/Colombo', _('Sri Lanka (Colombo) - GMT+5:30')
        # ASIA_KABUL = 'Asia/Kabul', _('Afghanistan (Kabul) - GMT+4:30')
        # ASIA_TEHRAN = 'Asia/Tehran', _('Iran (Tehran) - GMT+3:30')
        # ASIA_MUSCAT = 'Asia/Muscat', _('Oman (Muscat) - GMT+4')
        # ASIA_HO_CHI_MINH = 'Asia/Ho_Chi_Minh', _('Vietnam (Ho Chi Minh) - GMT+7')
        # ASIA_MANILA = 'Asia/Manila', _('Philippines (Manila) - GMT+8')
        # ASIA_KUALA_LUMPUR = 'Asia/Kuala_Lumpur', _('Malaysia (Kuala Lumpur) - GMT+8')
        # ASIA_JAKARTA = 'Asia/Jakarta', _('Indonesia (Jakarta) - GMT+7')
        # ASIA_TOKYO = 'Asia/Tokyo', _('Japan (Tokyo) - GMT+9')
        # ASIA_SEOUL = 'Asia/Seoul', _('South Korea (Seoul) - GMT+9')
        # ASIA_HONG_KONG = 'Asia/Hong_Kong', _('Hong Kong - GMT+8')
        # UTC = 'UTC', _('Coordinated Universal Time (UTC)')
    
    # ====================
    # LANGUAGES
    # ====================
    class LanguageChoices(models.TextChoices):
        BN = 'bn', _('Bangla (বাংলা)')
        EN = 'en', _('English')
        # AR = 'ar', _('Arabic (العربية)')
        # HI = 'hi', _('Hindi (हिन्दी)')
        # UR = 'ur', _('Urdu (اردو)')
        # FA = 'fa', _('Persian (فارسی)')
        # MY = 'my', _('Burmese (မြန်မာစာ)')
        # TH = 'th', _('Thai (ไทย)')
        # ZH_HANS = 'zh-hans', _('Chinese Simplified (简体中文)')
        # ZH_HANT = 'zh-hant', _('Chinese Traditional (繁體中文)')
        # JA = 'ja', _('Japanese (日本語)')
        # KO = 'ko', _('Korean (한국어)')
        # MS = 'ms', _('Malay (Bahasa Melayu)')
        # TA = 'ta', _('Tamil (தமிழ்)')
        # TE = 'te', _('Telugu (తెలుగు)')
        # ML = 'ml', _('Malayalam (മലയാളം)')
        # KN = 'kn', _('Kannada (ಕನ್ನಡ)')
        # GU = 'gu', _('Gujarati (ગુજરાતી)')
        # PA = 'pa', _('Punjabi (ਪੰਜਾਬੀ)')
        # MR = 'mr', _('Marathi (मराठी)')
        # OR = 'or', _('Odia (ଓଡ଼ିଆ)')
        # AS = 'as', _('Assamese (অসমীয়া)')
        # NE = 'ne', _('Nepali (नेपाली)')
        # SI = 'si', _('Sinhala (සිංහල)')
    
    # ====================
    # COUNTRIES (For Reference)
    # ====================
    class CountryChoices(models.TextChoices):
        BD = 'BD', _('Bangladesh')
        IN = 'IN', _('India')
        PK = 'PK', _('Pakistan')
        NP = 'NP', _('Nepal')
        BT = 'BT', _('Bhutan')
        MM = 'MM', _('Myanmar')
        LK = 'SL', _('Sri Lanka')
        MV = 'MV', _('Maldives')
        AF = 'AF', _('Afghanistan')
        IR = 'IR', _('Iran')
        SA = 'SA', _('Saudi Arabia')
        AE = 'AE', _('United Arab Emirates')
        OM = 'OM', _('Oman')
        QA = 'QA', _('Qatar')
        KW = 'KW', _('Kuwait')
        BH = 'BH', _('Bahrain')
        MY = 'MY', _('Malaysia')
        SG = 'SG', _('Singapore')
        TH = 'TH', _('Thailand')
        ID = 'ID', _('Indonesia')
        VN = 'VN', _('Vietnam')
        PH = 'PH', _('Philippines')
        CN = 'CN', _('China')
        JP = 'JP', _('Japan')
        KR = 'KR', _('South Korea')
        US = 'US', _('United States')
        GB = 'GB', _('United Kingdom')
        CA = 'CA', _('Canada')
        AU = 'AU', _('Australia')
        DE = 'DE', _('Germany')
        FR = 'FR', _('France')
        IT = 'IT', _('Italy')
        ES = 'ES', _('Spain')
    
    # ====================
    # BUSINESS TYPES (Bangladesh Specific)
    # ====================
    class BusinessTypeChoices(models.TextChoices):
        PRIVATE_LIMITED = 'private_limited', _('Private Limited Company')
        PUBLIC_LIMITED  = 'public_limited', _('Public Limited Company')
        PARTNERSHIP     = 'partnership', _('Partnership Firm')
        PROPRIETORSHIP  = 'proprietorship', _('Sole Proprietorship')
        JOINT_VENTURE   = 'joint_venture', _('Joint Venture')
        NGO             = 'ngo', _('Non-Government Organization (NGO)')
        TRUST           = 'trust', _('Trust')
        SOCIETY         = 'society', _('Society')
        GOVERNMENT      = 'government', _('Government Organization')
        MULTINATIONAL   = 'multinational', _('Multinational Company')
        FRANCHISE       = 'franchise', _('Franchise')
        COOPERATIVE     = 'cooperative', _('Cooperative Society')
    
    # ====================
    # INDUSTRY TYPES (Bangladesh Context)
    # ====================
    class IndustryChoices(models.TextChoices):
        GARMENTS       = 'garments', _('Ready Made Garments (RMG)')
        TEXTILE        = 'textile', _('Textile & Apparel')
        PHARMACEUTICAL = 'pharmaceutical', _('Pharmaceutical')
        AGRICULTURE    = 'agriculture', _('Agriculture & Farming')
        FISHERIES      = 'fisheries', _('Fisheries & Livestock')
        CONSTRUCTION   = 'construction', _('Construction & Real Estate')
        IT             = 'it', _('Information Technology')
        TELECOM        = 'telecom', _('Telecommunications')
        BANKING        = 'banking', _('Banking & Financial Services')
        INSURANCE      = 'insurance', _('Insurance')
        EDUCATION      = 'education', _('Education')
        HEALTHCARE     = 'healthcare', _('Healthcare & Hospitals')
        TRANSPORT      = 'transport', _('Transport & Logistics')
        MANUFACTURING  = 'manufacturing', _('Manufacturing')
        ENERGY         = 'energy', _('Energy & Power')
        LEATHER        = 'leather', _('Leather Goods')
        CERAMICS       = 'ceramics', _('Ceramics & Tiles')
        SHIPBUILDING   = 'shipbuilding', _('Shipbuilding')
        TOURISM        = 'tourism', _('Tourism & Hospitality')
        MEDIA          = 'media', _('Media & Entertainment')
        RETAIL         = 'retail', _('Retail & Wholesale')
        IMPORT_EXPORT  = 'import_export', _('Import & Export')
        CONSULTING     = 'consulting', _('Consulting Services')
        FREIGHT        = 'freight', _('Freight Forwarding')
        NGO            = 'ngo', _('NGO & Development')