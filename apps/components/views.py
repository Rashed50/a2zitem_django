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

from django.views.decorators.csrf import csrf_exempt

##? Import Models
User = get_user_model()



class FormTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'components/Form.html'


class TableTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'components/table.html'
    

class ButtonTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'components/button.html'
    

class BadgesTemplateView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('auth:login')
    template_name = 'components/badges.html'


#class TemplateView(LoginRequiredMixin, generic.TemplateView):
#     login_url = reverse_lazy('auth:login')
#     template_name = 'index.html'

#     def get_context_data(self, **kwargs):
#          context = super().get_context_data(**kwargs)
#          context['total_products'] = Product.objects.count()
#          context['user'] = self.request.user
#          return context



#class CreatePage(LoginRequiredMixin, generic.CreateView):
#     login_url     = reverse_lazy('auth:login')
#     template_name = 'create.html'
#     success_url   = reverse_lazy('your_app:list') 



#class ListPage(LoginRequiredMixin, generic.ListView):
#     model         = YourModel
#     template_name = 'list.html'
#     login_url     = reverse_lazy('auth:login')
#     context_object_name = 'objects'
#     paginate_by         = 25
#     ordering            = ['-created_at']



#class DetailPage(LoginRequiredMixin, generic.DetailView):
#     model         = YourModel
#     template_name = 'detail.html'
#     login_url     = reverse_lazy('auth:login')
#     context_object_name = 'object'



#class UpdatePage(LoginRequiredMixin, generic.UpdateView):
#     model         = YourModel
#     form_class    = YourForm
#     template_name = 'update.html'
#     login_url     = reverse_lazy('auth:login')
#     context_object_name = 'object'



