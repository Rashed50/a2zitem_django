from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
User = get_user_model()

from users.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

##? Models Import
from users.models import UserOTP


##! Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form     = UserChangeForm
    add_form = UserCreationForm

    list_display = ['id', 'email', 'first_name', 'last_name', 'phone', 'is_active', 'is_admin', 'is_superuser']
    list_filter  = ['is_superuser', 'is_admin', 'is_active', 'is_email_verified', 'is_phone_verified']

    fieldsets = [
        (None, {'fields': ['email', 'password', 'created_at', 'updated_at']}),
        ('Personal info', {'fields': [
            'first_name', 'last_name', 'phone', 'image', 'dob', 'blood_group', 'gender',
            'metadata'
        ]}),
        ('Religious info', {'fields': [
            'religion',
        ]}),
        ('Account info', {'fields': [
            'signup_ip', 'signup_source', 'timezone', 'language_preference', 'fcm_device_token', 'last_activity'
        ]}),
        ('Permissions', {'fields': [
            'is_admin', 'is_active', 'is_superuser',   
            'is_email_verified', 'email_verified_at',
            'is_phone_verified', 'phone_verified_at',
            'two_factor_enabled', 
            'failed_login_attempts', 'lockout_until',
            'groups', 'user_permissions'                   ##* groups & permissions
        ]}),
        ('Password info', {'fields': ['password_changed_at', 'auth_provider']}),
    ]

    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': [
                    'email', 'password', 'password2',
                    'first_name', 'last_name', 'phone', 'image', 'dob', 'blood_group', 'gender', 
                    'religion', 
                    'metadata',
                    'signup_ip', 'signup_source', 'timezone', 'language_preference', 'fcm_device_token',
                    'is_admin', 'is_active', 'is_superuser', 
                    'is_email_verified', 'is_phone_verified', 'two_factor_enabled',
                    'groups', 'user_permissions'
                ]
            }
        ),
    ]

    readonly_fields = [
        'created_at', 'updated_at', 'email_verified_at', 'phone_verified_at', 'last_activity', 'password_changed_at'
    ]

    search_fields = [
        'email__icontains',
        'phone__icontains',
        'first_name__icontains',
        'last_name__icontains',
    ]
    ordering            = ['-created_at', 'email']
    autocomplete_fields = ['religion']
    filter_horizontal   = ['groups', 'user_permissions']  ##* Only needed for ManyToMany fields
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['reset_password_url'] = f'./{object_id}/password/'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(UserOTP)    
class UserOTPAdmin(admin.ModelAdmin):
    list_display        = ['id', 'user', 'otp', 'is_otp_used', 'is_token_used', 'created_at',]
    # readonly_fields   = ['user', 'otp', 'created_at', 'updated_at']
    search_fields       = ['user__email', 'user__phone']
    autocomplete_fields = ['user']
    ordering            = ['-created_at']
    
    




##! Now register the new UserAdmin...
# admin.site.register(User)
# admin.site.unregister(Group)


# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display  = ['id', 'name']   
#     search_fields = ['name']        
#     ordering      = ['id']            

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
        name         : Human-readable name of the permission (eg. 'Can view users')
        content_type : Indicates which model this permission is linked to. (eg. 'user')
        codename     : Unique slug for use in code (eg. 'view_users')
    """
    
    list_display  = ['id', 'name', 'codename', 'content_type']  
    search_fields = ['name', 'codename']
    list_filter   = ['content_type']  
    ordering      = ['id']


"""
<link rel="stylesheet" href="{% static 'css/project.css' %}?{% now "U" %}">
This uses the {% now "U" %} template tag to generate a unique timestamp each time the page is loaded, effectively bypassing the cache for your CSS files.
"""