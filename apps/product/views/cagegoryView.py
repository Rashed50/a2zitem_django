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
from apps.product.models.category import Category


class CategoryListPageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'category/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_choices = Category.objects.filter(
                is_deleted=False, parent__isnull=True,
            ).values_list('id', 'name')
        category_data = [
                {'value': choice[0], 'label': str(choice[1])} 
                for choice in category_choices
            ]
        status_data = [
            {'value': True, 'label': 'Active'},
            {'value': False, 'label': 'Inactive'},
        ]
        context['category_json'] = mark_safe(json.dumps(category_data, ensure_ascii=False))
        context['status_json'] = mark_safe(json.dumps(status_data, ensure_ascii=False))
        return context


class CategoryCreatePageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'category/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user    = self.request.user
        root_category_choices = Category.objects.filter(
                is_deleted=False, parent__isnull=True,
            ).values_list('id', 'name')
        root_category_data = [
                {'value': choice[0], 'label': str(choice[1])} 
                for choice in root_category_choices
            ]

        context['root_category_json'] = mark_safe(json.dumps(root_category_data, ensure_ascii=False))
        return context