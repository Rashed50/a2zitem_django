import uuid, secrets, random
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from users.manager import UserManager

from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

##? Utils Import
from users.validators import DateOfBirthValidator, ImageValidator

##? Models Import 
from core.models.time_stamped import TimestampedModel, TimestampedModel2
from core.models.religion_model import Religion, ReligionDenomination
from core.models.address_model import Country, State, City

##? Utils Import
from core.utils.field_error_messages import get_field_error_messages


##! AbstructBaseUser has provite some default field ( password, last_login, is_active )
class User(AbstractBaseUser, TimestampedModel, PermissionsMixin):

    class GenderType(models.TextChoices):
        MALE    = 'male',   _('Male')
        FEMALE  = 'female', _('Female')
        OTHERS  = 'others', _('Others')
    
    class AuthProvider(models.TextChoices):
        LOCAL     = 'local',     _('Local')
        GOOGLE    = 'google',    _('Google')
        FACEBOOK  = 'facebook',  _('Facebook')
        TWITTER   = 'twitter',   _('Twitter')
        INSTAGRAM = 'instagram', _('Instagram')
        LINKEDIN  = 'linkedIn',  _('LinkedIn')
        GITHUB    = 'gitHub',    _('GitHub')

    id  = models.UUIDField(
            verbose_name = _("ID"), 
            primary_key  = True, 
            unique       = True, 
            default      = uuid.uuid4, 
            editable     = False 
        )
    
    slug = models.SlugField(
            verbose_name = _("Slug"), 
            unique       = True, 
            null         = True,
            blank        = True, 
        )

    email = models.EmailField(
            verbose_name = _("Email address"),
            unique       = True,
            max_length   = 255,
            db_index     = True,
            validators   = [EmailValidator(message=_("Enter a valid email address."))],
            error_messages = get_field_error_messages(_('Email'), 'EmailField')
        )
    
    phone = models.CharField(
            verbose_name = _("Phone number"),
            unique       = True,
            max_length   = 30,
            null         = True,
            blank        = True,
            db_index     = True
        )
    
    first_name = models.CharField(
            verbose_name = _("First name"), 
            max_length   = 255, 
            null         = True, 
            blank        = True,
            validators   = [MinLengthValidator(2, message=_("First name must be at least 2 characters long."))]
        )

    last_name  = models.CharField(
            verbose_name = _("Last name"), 
            max_length   = 255, 
            null         = True, 
            blank        = True,
            validators   = [MinLengthValidator(2, message=_("First name must be at least 2 characters long."))]
        )

    gender = models.CharField(
            verbose_name = _("Gender"), 
            max_length   = 10, 
            choices      = GenderType.choices, 
            null         = True, 
            blank        = True,
        )
     
    dob = models.DateField(
            verbose_name = _("Date of birth"), 
            null         = True, 
            blank        = True,
            validators   = [DateOfBirthValidator]
        )
    
    blood_group = models.CharField(
            verbose_name = _("Blood Group"), 
            max_length   = 10, 
            null         = True, 
            blank        = True,
        )

    image = models.ImageField(
            verbose_name = _("Profile Image"), 
            upload_to    = "Users/ProfileImage/", 
            null         = True, 
            blank        = True,
            validators   = [ImageValidator]
        )

    ## User Permission and Roll
    is_active   = models.BooleanField(verbose_name=_("Active"), default = True)
    is_admin    = models.BooleanField(verbose_name=_("Admin"), default = False)

    is_email_verified = models.BooleanField(verbose_name=_("Email Verification"), default = False)
    email_verified_at = models.DateTimeField(verbose_name=_("Email Verification Time"), null=True, blank=True)

    is_phone_verified = models.BooleanField(verbose_name=_("Phone Verification"), default = False)
    phone_verified_at = models.DateTimeField(verbose_name=_("Phone Verification Time"), null=True, blank=True)

    auth_provider = models.CharField(  
            verbose_name = _("Authentication With"),
            max_length   = 20, 
            choices      = AuthProvider.choices, 
            default      = AuthProvider.LOCAL
        )

    fcm_device_token = models.TextField(
            verbose_name = _("Device Token"), 
            blank        = True,
            null         = True
        )
    
    ##! Foreign Keys
    religion = models.ForeignKey(
            Religion, 
            null         = True, 
            blank        = True, 
            on_delete    = models.SET_NULL,
            verbose_name = _("User Religion"),
        )

    ##! Additional info
    metadata = models.JSONField(
        verbose_name = _("Metadata"),
        default      = dict,
        null         = True,
        blank        = True,
        help_text    = _("Flexible JSON field to store additional user-related information.")
    )

    last_activity = models.DateTimeField(
        verbose_name = _("Last Activity"),
        null         = True,
        blank        = True,
        help_text    = _("Timestamp of the user's last activity on the system.")
    )

    signup_ip = models.GenericIPAddressField(
        verbose_name = _("Signup IP Address"),
        null         = True,
        blank        = True,
        help_text    = _("IP address from which the user signed up.")
    )

    signup_source = models.CharField(
        verbose_name = _("Signup Source"),
        max_length   = 50,
        null         = True,
        blank        = True,
        help_text    = _("Source platform or method used for user signup (e.g., web, mobile app).")
    )

    timezone = models.CharField(
        verbose_name = _("Timezone"),
        max_length   = 50,
        default      = "UTC",
        help_text    = _("User's preferred timezone for displaying times and dates.")
    )

    language_preference = models.CharField(
        verbose_name = _("Language Preference"),
        max_length   = 10,
        default      = "en",
        help_text    = _("User's preferred language for the system interface.")
    )

    two_factor_enabled = models.BooleanField(
        verbose_name = _("Two-Factor Authentication Enabled"),
        default      = False,
        help_text    = _("Indicates whether two-factor authentication is enabled for the user.")
    )

    password_changed_at = models.DateTimeField(
        verbose_name = _("Password Changed At"),
        null         = True,
        blank        = True,
        help_text    = _("Timestamp when the user last changed their password.")
    )

    failed_login_attempts = models.PositiveIntegerField(
        verbose_name = _("Failed Login Attempts"),
        default      = 0,
        help_text    = _("Number of consecutive failed login attempts.")
    )

    lockout_until = models.DateTimeField(
        verbose_name = _("Lockout Until"),
        null         = True,
        blank        = True,
        help_text    = _("Timestamp until which the user account is locked due to multiple failed login attempts.")
    )

    objects = UserManager()

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ['phone']

    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Superusers always have all permissions.
        Otherwise, check actual Django permission system.
        """
        if getattr(self, "is_superuser", False):
            return True
        return super().has_perm(perm, obj=obj)

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        if getattr(self, "is_superuser", False):
            return True
        return super().has_module_perms(app_label)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def is_customer(self):
        return not self.is_admin and not self.is_superuser

    @property
    def is_verified(self): # email_verified_at or phone_verified_at
        return self.is_email_verified or self.is_phone_verified

    @property
    def get_full_name(self):
        parts = [self.first_name or '', self.last_name or '']
        return " ".join(part for part in parts if part).strip()
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def f_name(self):
        if self.first_name:
            return self.first_name
        return None

    @property
    def l_name(self):
        if self.last_name:
            return self.last_name
        return None

    @property
    def age(self):
        if self.dob:
            # today = datetime.date.today()  ## NOTE:- Automatic Handling of Timezones
            today = timezone.now().date()    ## NOTE:- Integration with Django Settings `TIME_ZONE `

            age   = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        else:
            return None
        
    @property
    def name_and_email(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.email})"
        if self.first_name:
            return f"{self.first_name} ({self.email})"
        if self.last_name:
            return f"{self.last_name} ({self.email})"
        return self.email
    
    @property
    def created_date(self):  ## NOTE:- Date DD/MM/YYYY Ex: 15/01/2023
        if self.created_at:
            local_time = timezone.localtime(self.created_at)
            return local_time.strftime("%d %b %Y")
        return None
    
    @property
    def updated_date(self):  ## NOTE:- Date DD/MM/YYYY Ex: 29/08/2023
        if self.updated_at:
            local_time = timezone.localtime(self.updated_at)
            return local_time.strftime("%d %b %Y")
        return None
        
    @property
    def created_date_time(self):  ## NOTE:- Time DD/MM/YYYY HH:MM  Ex: 15/01/2023 02:44:AM
        if self.created_at:
            local_time = timezone.localtime(self.created_at)
            return local_time.strftime("%d %b %Y %I:%M %p")
        return None
    
    @property
    def updated_date_time(self):  ## NOTE:- Time DD/MM/YYYY HH:MM Ex: 29/08/2023 11:30:PM
        if self.updated_at:
            local_time = timezone.localtime(self.updated_at)
            return local_time.strftime("%d %b %Y %I:%M %p")
        return None

    @property
    def last_login_date_time(self):  ## NOTE:- Time DD/MM/YYYY HH:MM Ex: 29/08/2023 11:30:PM
        if self.last_login:
            local_time = timezone.localtime(self.last_login)
            return local_time.strftime("%d %b %Y %I:%M %p")
        return None

    @property
    def is_incomplete(self):
        ## NOTE:- Check if any of the required fields are missing then say profile is incomplete
        required_fields = [
            self.first_name, 
            self.last_name, 
            self.phone, 
            self.dob, 
            self.gender, 
            self.religion
        ]
        return any(field in (None, '') for field in required_fields)
    
    def save(self, *args, **kwargs):

        ## NOTE:- Save The Slug 
        if not self.slug:
            # base_slug = slugify(f"{self.first_name}-{self.last_name}-{self.email.split('@')[0]}")
            base_slug = slugify(f"{self.email.split('@')[0]}")
            slug = base_slug
            count = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        ## NOTE:- Save email_verified_at when is_email_verified = True
        if self.is_email_verified and not self.email_verified_at:
            self.email_verified_at = timezone.now()
        

        ## NOTE:- Save phone_verified_at when is_phone_verified = True
        if self.is_phone_verified and not self.phone_verified_at:
            self.phone_verified_at = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        # db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users') 

##! User OTP
class UserOTP(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otp",
        verbose_name="User"
    )

    otp = models.IntegerField(
        verbose_name="OTP Code",
        validators=[
            MinValueValidator(100000, message="OTP must be a 6-digit number."),
            MaxValueValidator(999999, message="OTP must be a 6-digit number.")
        ]
    )

    token = models.CharField(
        verbose_name="Token",
        max_length=100,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9-_]{64}$',
                message="Token must be a valid 64-character string."
            )
        ]
    )

    is_otp_used = models.BooleanField(
        verbose_name = "Is OTP Used",
        default      = False,
    )

    is_token_used = models.BooleanField(
        verbose_name = "Is Token Used",
        default      = False,
    )
    
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.email} - {self.otp}"

    def generate_token(self):
        # generate 64-character token
        token = secrets.token_urlsafe(48)  # 48 bytes give approximately 64 characters when URL-safe encoded
        return token

    def generate_code(self):
        # generate 6-digit OTP
        # otp = random.randint(100000, 999999)
        # return str(otp).zfill(6)
        return random.randint(100000, 999999)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_code()

        if not self.token:
            self.token = self.generate_token()
            
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(
                minutes=settings.OTP_TIMEOUT
            )
        super().save(*args, **kwargs)

    @property
    def is_otp_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def is_token_expired(self):
        return timezone.now() > (
            self.created_at + timezone.timedelta(minutes=settings.OTP_TOKEN_TIMEOUT)
        )
        
    @property
    def expiry_time(self):
        # return timezone.localtime(self.expires_at).strftime("%d %b %Y %I:%M %p")
        return timezone.localtime(self.expires_at).strftime("%Y-%m-%d %I:%M %p")
    
    @property
    def created_time(self):
        return timezone.localtime(self.created_at).strftime("%Y-%m-%d %I:%M %p")
    
    class Meta:
        verbose_name = "User OTP"
        verbose_name_plural = "User OTPs"


