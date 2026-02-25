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
from django.contrib.auth.models import Group, Permission


##? Import Models
User = get_user_model()

class RolesListPageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'roles/list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         return context


class RoleCreatePageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'roles/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # request_user        = self.request.user
        # gender_choices      = User.GenderType.choices
        # blood_group_choices = UserChoices.BloodGroupChoices.choices
        # gender_data      = [{'value': choice[0], 'label': str(choice[1])} for choice in gender_choices]
        # blood_group_data = [{'value': choice[0], 'label': str(choice[1])} for choice in blood_group_choices]
        # context['gender_json']      = mark_safe(json.dumps(gender_data, ensure_ascii=False))
        # context['blood_group_json'] = mark_safe(json.dumps(blood_group_data, ensure_ascii=False))
        return context



class RoleDetailsPageView(LoginRequiredMixin, generic.DetailView):
    model         = Group
    template_name = 'roles/details.html'
    login_url     = reverse_lazy('auth:login')
    context_object_name = 'object'


class RoleUpdatePageView(LoginRequiredMixin, generic.DetailView):
    model         = Group
    template_name = 'roles/update.html'
    login_url     = reverse_lazy('auth:login')
    context_object_name = 'object'
    


class PermmissionsListPageView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'permissions/list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         return context