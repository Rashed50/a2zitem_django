import uuid, json, random, datetime
from django.db import models
from django.conf import settings

from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from datetime import timedelta
from django.contrib.auth import get_user_model

##? Import Users
User = get_user_model() 

##? Import TimestampedModel 
from core.models.time_stamped import TimestampedModel


#class YourModelName(TimestampedModel): 
#     pass 
