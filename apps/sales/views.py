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

##? Models Import
User = get_user_model()
from apps.product.models.product import Product
from apps.product.models.variant import ProductVariant
from apps.product.models.brand import Brand
from apps.product.models.category import Category
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.sales.models.sale import Sale

class SaleListPageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'sale/list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         return context
     
     
class SaleCreatePageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'sale/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SaleDetailPageView(LoginRequiredMixin, generic.DetailView):
    model = Sale
    login_url = reverse_lazy('auth:login')
    template_name = 'sale/detail.html'
    context_object_name = 'object'


class SaleUpdatePageView(LoginRequiredMixin, generic.DetailView):
    model         = Sale
    template_name = 'sale/update.html'
    login_url     = reverse_lazy('auth:login')
    context_object_name = 'object'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_choices    = Brand.objects.filter(is_deleted=False, is_active=True).values_list('id', 'name')
        coloer_choices   = Color.objects.filter(is_deleted=False, is_active=True).values_list('id', 'name')
        size_choices     = Size.objects.filter(is_deleted=False, is_active=True).values_list('id', 'name')
        unit_choices     = UnitOfMeasure.objects.filter(is_deleted=False, is_active=True).values_list('id', 'name')
        category_choices = Category.objects.filter(
                is_deleted=False, is_active=True, parent__isnull=True
            ).values_list('id', 'name')
        
        brand_data    = [{'value': choice[0], 'label': str(choice[1])} for choice in brand_choices]
        color_data    = [{'value': choice[0], 'label': str(choice[1])} for choice in coloer_choices]
        size_data     = [{'value': choice[0], 'label': str(choice[1])} for choice in size_choices]
        unit_data     = [{'value': choice[0], 'label': str(choice[1])} for choice in unit_choices]
        category_data = [{'value': choice[0], 'label': str(choice[1])} for choice in category_choices]
        status_data = [
            {'value': 'true', 'label': 'Active'},
            {'value': 'false', 'label': 'Inactive'},
        ]
        
        # context['brand_json']    = mark_safe(json.dumps(brand_data, ensure_ascii=False))
        # context['category_json'] = mark_safe(json.dumps(category_data, ensure_ascii=False))
        # context['status_json']   = mark_safe(json.dumps(status_data, ensure_ascii=False))
        
        context["page_data"] = {
            "brands"     : brand_data,
            "colors"     : color_data,
            "sizes"      : size_data,
            "units"      : unit_data,
            "categories" : category_data,
            "statuses"   : status_data,
        }
        
        # print("===========================")
        # print(brand_data)
        # print("===========================")
        return context