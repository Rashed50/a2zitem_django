import json, random, decimal, time
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.views import View, generic
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session

from django.db.models.functions import Concat, ExtractMonth, ExtractYear
from django.db.models import Q, Count, F, Value as V, CharField, Sum

from django.http import HttpRequest, HttpResponse, JsonResponse, Http404, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group

##? Utils Import
from core.constants import UserChoices

##? Import Models
User = get_user_model()
from apps.supplier.models import Supplier


class SupplierListPageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'supplier/list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         return context


class SupplierCreatePageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'supplier/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user    = self.request.user
        # company_choices = Company.objects.filter(is_deleted=False, is_active=True)\
        #                                      .values_list('id', 'name')
        # if not request_user.is_superuser:                            
        #     employee_profile = getattr(request_user, 'employee', None)
        #     if employee_profile and employee_profile.company:
        #         company_choices = company_choices.filter(id=employee_profile.company.id)
        #     else:
        #         company_choices = Company.objects.none()
                
        # company_data = [
        #     {'value': choice[0], 'label': str(choice[1])} 
        #     for choice in company_choices
        # ]
        # context['company_json'] = mark_safe(json.dumps(company_data, ensure_ascii=False))
        return context



class SupplierDetailsPageView(LoginRequiredMixin, generic.DetailView):
    model         = Supplier
    template_name = 'supplier/details.html'
    login_url     = reverse_lazy('auth:login')
    context_object_name = 'object'


class SupplierUpdatePageView(LoginRequiredMixin, generic.DetailView):
    model         = Supplier
    template_name = 'supplier/update.html'
    login_url     = reverse_lazy('auth:login')
    context_object_name = 'object'