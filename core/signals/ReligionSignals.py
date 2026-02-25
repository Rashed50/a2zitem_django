from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

from core.models.religion_model import Religion, ReligionDenomination


RELIGION_DATA = {
    'Islam': [
        'Sunni',
        'Shia',
        'Ahmadi',
        'Sufi',
        'Others',
    ],
    'Christian': [
        'Catholic',
        'Protestant',
        'Orthodox',
        'Non-Denominational',
        'Others',
    ],
    'Hindu': [
        'Vaishnavism',
        'Shaivism',
        'Shaktism',
        'Smartism',
        'Others',
    ],
    'Buddhist': [
        'Theravada',
        'Mahayana',
        'Vajrayana',
        'Zen',
        'Others',
    ],
    'Others': [
        'Others',
    ],
}

@receiver(post_migrate)
def seed_religions_and_denominations(sender, **kwargs):
    
    if sender.name != 'core':
        return

    for religion_name, denominations in RELIGION_DATA.items():

        religion, _ = Religion.objects.get_or_create(
            name=religion_name
        )

        for denomination_name in denominations:
            ReligionDenomination.objects.get_or_create(
                religion=religion,
                name=denomination_name
            )

