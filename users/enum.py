from django.db import models
from django.utils.translation import gettext_lazy as _

class ReligionType(models.TextChoices):
    ISLAM     = 'Islam',     _('Islam')
    HINDU     = 'Hindu',     _('Hindu')
    CHRISTIAN = 'Christian', _('Christian')
    BUDDHIST  = 'Buddhist',  _('Buddhist')
    OTHERS    = 'Others',    _('Others')

class ChristianDenomination(models.TextChoices):
    CATHOLIC            = 'Catholic',            _('Catholic')
    PROTESTANT          = 'Protestant',          _('Protestant')
    ORTHODOX            = 'Orthodox',            _('Orthodox')
    NON_DENOMINATIONAL  = 'Non-Denominational',  _('Non-Denominational')
    OTHERS              = 'Others',              _('Others')

class IslamicDenomination(models.TextChoices):
    SUNNI     = 'Sunni',     _('Sunni')
    SHIA      = 'Shia',      _('Shia')
    AHMADI    = 'Ahmadi',    _('Ahmadi')
    SUFI      = 'Sufi',      _('Sufi')
    OTHERS    = 'Others',    _('Others')

class HinduDenomination(models.TextChoices):
    VAISHNAVISM = 'Vaishnavism', _('Vaishnavism')
    SHAIVISM    = 'Shaivism',    _('Shaivism')
    SHAKTISM    = 'Shaktism',    _('Shaktism')
    SMARTISM    = 'Smartism',    _('Smartism')
    OTHERS      = 'Others',      _('Others')

class BuddhistDenomination(models.TextChoices):
    THERAVADA  = 'Theravada',  _('Theravada')
    MAHAYANA   = 'Mahayana',   _('Mahayana')
    VAJRAYANA  = 'Vajrayana',  _('Vajrayana')
    ZEN        = 'Zen',        _('Zen')
    OTHERS     = 'Others',     _('Others')