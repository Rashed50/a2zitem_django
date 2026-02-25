from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

from core.models.address_model import Country, State, City


COUNTRY_DATA = {
    'Bangladesh': {  
        'Dhaka'      : ['Dhaka', 'Gazipur', 'Narayanganj', 'Tangail'],
        'Chittagong' : ['Chittagong', 'Cox\'s Bazar', 'Comilla', 'Feni'],
        'Rajshahi'   : ['Rajshahi', 'Bogra', 'Pabna'],
        'Khulna'     : ['Khulna', 'Jessore', 'Satkhira'],
        'Sylhet'     : ['Sylhet', 'Moulvibazar', 'Sunamganj'],
        'Barisal'    : ['Barisal', 'Patuakhali', 'Bhola'],
        'Rangpur'    : ['Rangpur', 'Dinajpur', 'Gaibandha'],
        'Mymensingh' : ['Mymensingh', 'Jamalpur', 'Netrokona'],
    },
    'United States': {  
        'California'   : ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'San Jose'],
        'Texas'        : ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
        'Florida'      : ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
        'New York'     : ['New York City', 'Buffalo', 'Rochester', 'Albany'],
        'Illinois'     : ['Chicago', 'Springfield', 'Peoria', 'Rockford'],
        'Pennsylvania' : ['Philadelphia', 'Pittsburgh', 'Harrisburg'],
    },
    'India': {  
        'Maharashtra'   : ['Mumbai', 'Pune', 'Nagpur', 'Nashik'],
        'Uttar Pradesh' : ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Prayagraj'],
        'Karnataka'     : ['Bangalore', 'Mysore', 'Hubli', 'Mangalore'],
        'Tamil Nadu'    : ['Chennai', 'Coimbatore', 'Madurai', 'Salem'],
        'Gujarat'       : ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot'],
        'West Bengal'   : ['Kolkata', 'Howrah', 'Durgapur', 'Asansol'],
        'Rajasthan'     : ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota'],
    },
    'France': {  
        'Île-de-France'               : ['Paris', 'Versailles', 'Boulogne-Billancourt'],
        'Auvergne-Rhône-Alpes'        : ['Lyon', 'Grenoble', 'Saint-Étienne', 'Clermont-Ferrand'],
        'Provence-Alpes-Côte d\'Azur' : ['Marseille', 'Nice', 'Toulon', 'Aix-en-Provence'],
        'Nouvelle-Aquitaine'          : ['Bordeaux', 'Limoges', 'Poitiers'],
        'Occitanie'                   : ['Toulouse', 'Montpellier', 'Nîmes'],
        'Hauts-de-France'             : ['Lille', 'Amiens', 'Roubaix'],
    },
    'Germany': {  
        'Bavaria'                : ['Munich', 'Nuremberg', 'Augsburg', 'Regensburg'],
        'North Rhine-Westphalia' : ['Cologne', 'Düsseldorf', 'Dortmund', 'Essen', 'Bonn'],
        'Baden-Württemberg'      : ['Stuttgart', 'Karlsruhe', 'Mannheim', 'Freiburg'],
        'Hesse'                  : ['Frankfurt', 'Wiesbaden', 'Kassel'],
        'Lower Saxony'           : ['Hanover', 'Braunschweig', 'Oldenburg'],
        'Berlin'                 : ['Berlin'],  
        'Hamburg'                : ['Hamburg'],  
    },
}


COUNTRY_BASIC_DATA = {
    'Bangladesh' : {
        'code'       : 'BD',
        'capital'    : 'Dhaka',
        'cur_code'   : 'BDT',
        'cur_name'   : 'Bangladeshi Taka',
        'cur_symbol' : '৳',
        'dia_code'   : '+880',
        'iso_code'   : 'BD',
        'states': {
            'Dhaka'      : ['Dhaka', 'Gazipur', 'Narayanganj', 'Tangail'],
            'Chittagong' : ['Chittagong', 'Cox\'s Bazar', 'Comilla', 'Feni'],
            'Rajshahi'   : ['Rajshahi', 'Bogra', 'Pabna'],
            'Khulna'     : ['Khulna', 'Jessore', 'Satkhira'],
            'Sylhet'     : ['Sylhet', 'Moulvibazar', 'Sunamganj'],
            'Barisal'    : ['Barisal', 'Patuakhali', 'Bhola'],
            'Rangpur'    : ['Rangpur', 'Dinajpur', 'Gaibandha'],
            'Mymensingh' : ['Mymensingh', 'Jamalpur', 'Netrokona'],
        }
    },
    'United States': {
        'code'       : 'US',
        'capital'    : 'Washington, D.C.',
        'cur_code'   : 'USD',
        'cur_name'   : 'United States Dollar',
        'cur_symbol' : '$',
        'dia_code'   : '+1',
        'iso_code'   : 'US',
        'states': {
            'California'   : ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'San Jose'],
            'Texas'        : ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
            'Florida'      : ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
            'New York'     : ['New York City', 'Buffalo', 'Rochester', 'Albany'],
            'Illinois'     : ['Chicago', 'Springfield', 'Peoria', 'Rockford'],
            'Pennsylvania' : ['Philadelphia', 'Pittsburgh', 'Harrisburg'],
        }
    },
    'India': {
        'code'       : 'IN',
        'capital'    : 'New Delhi',
        'cur_code'   : 'INR',
        'cur_name'   : 'Indian Rupee',
        'cur_symbol' : '₹',
        'dia_code'   : '+91',
        'iso_code'   : 'IN',
        'states': {
            'Maharashtra'   : ['Mumbai', 'Pune', 'Nagpur', 'Nashik'],
            'Uttar Pradesh' : ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Prayagraj'],
            'Karnataka'     : ['Bangalore', 'Mysore', 'Hubli', 'Mangalore'],
            'Tamil Nadu'    : ['Chennai', 'Coimbatore', 'Madurai', 'Salem'],
            'Gujarat'       : ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot'],
            'West Bengal'   : ['Kolkata', 'Howrah', 'Durgapur', 'Asansol'],
            'Rajasthan'     : ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota'],
        }
    },
    'France': {
        'code'      : 'FR',
        'capital'   : 'Paris',
        'cur_code'  : 'EUR',
        'cur_name'  : 'Euro',
        'cur_symbol': '€',
        'dia_code'  : '+33',
        'iso_code'  : 'FR',
        'states': {
            'Île-de-France'               : ['Paris', 'Versailles', 'Boulogne-Billancourt'],
            'Auvergne-Rhône-Alpes'        : ['Lyon', 'Grenoble', 'Saint-Étienne', 'Clermont-Ferrand'],
            'Provence-Alpes-Côte d\'Azur' : ['Marseille', 'Nice', 'Toulon', 'Aix-en-Provence'],
            'Nouvelle-Aquitaine'          : ['Bordeaux', 'Limoges', 'Poitiers'],
            'Occitanie'                   : ['Toulouse', 'Montpellier', 'Nîmes'],
            'Hauts-de-France'             : ['Lille', 'Amiens', 'Roubaix'],
        }
    },
    'Germany': {
        'code'       : 'DE',
        'capital'    : 'Berlin',
        'cur_code'   : 'EUR',
        'cur_name'   : 'Euro',
        'cur_symbol' : '€',
        'dia_code'   : '+49',
        'iso_code'   : 'DE',
        'states': {
            'Bavaria'                : ['Munich', 'Nuremberg', 'Augsburg', 'Regensburg'],
            'North Rhine-Westphalia' : ['Cologne', 'Düsseldorf', 'Dortmund', 'Essen', 'Bonn'],
            'Baden-Württemberg'      : ['Stuttgart', 'Karlsruhe', 'Mannheim', 'Freiburg'],
            'Hesse'                  : ['Frankfurt', 'Wiesbaden', 'Kassel'],
            'Lower Saxony'           : ['Hanover', 'Braunschweig', 'Oldenburg'],
            'Berlin'                 : ['Berlin'],
            'Hamburg'                : ['Hamburg'],
        }
    },
}

@receiver(post_migrate)
def seed_countries_states_and_cities(sender, **kwargs):
    if sender.name != 'core':
        return

    Country = apps.get_model('core', 'Country')
    State   = apps.get_model('core', 'State')
    City    = apps.get_model('core', 'City')

    for country_name, data in COUNTRY_BASIC_DATA.items():
        country_obj, country_created = Country.objects.get_or_create(
            name     = country_name,
            defaults = {
                'code'       : data['code'],
                'capital'    : data['capital'],
                'cur_code'   : data['cur_code'],
                'cur_name'   : data['cur_name'],
                'cur_symbol' : data['cur_symbol'],
                'dia_code'   : data['dia_code'],
                'iso_code'   : data['iso_code'],
            }
        )

        if country_created:
            print(f"Created Country: {country_name}")
        else:
            print(f"Country already exists: {country_name}")

        ## Now seed states and cities
        for state_name, cities in data['states'].items():
            state_obj, state_created = State.objects.get_or_create(
                country = country_obj,
                name    = state_name
            )
            if state_created:
                print(f"   Created State: {state_name}")

            for city_name in cities:
                City.objects.get_or_create(
                    state = state_obj,
                    name  = city_name
                )
                # print(f"      Created City: {city_name}")  # অনেক হলে কমেন্ট আউট করো

    print("🌍 Country, State & City seeding completed successfully!")