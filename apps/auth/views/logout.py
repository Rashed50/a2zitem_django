from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.utils.translation import gettext as _

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return self.logout_user(request)
    
    def post(self, request, *args, **kwargs):
        return self.logout_user(request)
    
    def logout_user(self, request):
        # Store success message before logout (messages framework works with authenticated users)
        messages.success(request, _('You have been successfully logged out.'))
        
        # Perform logout
        logout(request)
        
        # Clear session completely
        request.session.flush()
        
        # Redirect to login page or next URL
        next_url = request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
            return redirect(next_url)
        
        return redirect('auth:login')