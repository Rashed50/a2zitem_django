from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext as _
import re

class AdminSingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Pre-compile regex patterns for better performance
        self.admin_regex_patterns = [
            re.compile(r'^/admin/'),
            re.compile(r'^/dashboard/admin/'),
            re.compile(r'^/api/v\d+/admin/'),
            re.compile(r'^/manager/'),
            re.compile(r'^/system/'),
            re.compile(r'^/settings/'),
            re.compile(r'^/analytics/'),
            re.compile(r'^/reports/'),
        ]
        
        self.fixed_admin_paths = [
            '/admin/', '/dashboard/admin/', '/manager/', 
            '/supervisor/', '/system-admin/', '/control-panel/'
        ]

    def __call__(self, request):
        # Early return if not authenticated or not admin route
        if not request.user.is_authenticated:
            return self.get_response(request)
            
        if not self.is_admin_dashboard_request(request):
            return self.get_response(request)
            
        if not hasattr(request.user, 'admin_current_session_key'):
            return self.get_response(request)
            
        current_admin_session = getattr(request.user, 'admin_current_session_key', None)
        
        # Check if this session is not the current active admin session
        if current_admin_session and current_admin_session != request.session.session_key:
            return self.handle_session_conflict(request)
            
        return self.get_response(request)

    def handle_session_conflict(self, request):
        """Handle session conflict by logging out and redirecting"""
        # Store user email for logging
        user_email = request.user.email
        
        # Logout the user
        logout(request)
        
        # Clear the session
        request.session.flush()
        
        # Add error message
        messages.error(request, _('Your admin account has been logged in from another device. Please login again.'))
        
        # Log the session conflict (optional)
        print(f"Session conflict detected for admin user: {user_email}")
        
        # Redirect to admin login page
        from django.shortcuts import redirect
        return redirect('auth:admin_login')

    def is_admin_dashboard_request(self, request):
        """Combined smart detection for admin routes"""
        current_path = request.path
        
        # 1. Quick check with fixed paths (fastest)
        if any(current_path.startswith(path) for path in self.fixed_admin_paths):
            return True
        
        # 2. Check regex patterns
        if any(pattern.match(current_path) for pattern in self.admin_regex_patterns):
            return True
        
        # 3. Check if user is admin and accessing privileged areas
        if (self.is_admin_user(request.user) and 
            self.is_privileged_area(request)):
            return True
        
        return False

    def is_admin_user(self, user):
        """Check if user has admin privileges"""
        return (user.is_authenticated and 
               (user.is_superuser or user.is_staff or getattr(user, 'is_admin', False)))

    def is_privileged_area(self, request):
        """Check if the request is for privileged areas"""
        current_path = request.path.lower()
        privileged_keywords = [
            'dashboard', 'analytics', 'reports', 
            'settings', 'management', 'control',
            'admin', 'manager', 'system'
        ]
        
        return any(keyword in current_path for keyword in privileged_keywords)