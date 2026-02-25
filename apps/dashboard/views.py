import json, random, time
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views import View, generic
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.urls import reverse, reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

# Create your views here.
class Home(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy("auth:login")
    redirect_field_name = "login"
    # template_name = 'home.html'
    # template_name = 'layouts/master.html'
    template_name = 'dashboard/home.html'
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     # Add your custom context data here
    #     context["total_user"] = User.objects.all().count()
    #     context["total_chalan"] = Chalan.objects.all().count()
    #     context["total_inbound"] = InboundCourier.objects.all().count()
    #     context["total_outbound"] = OutboundCourier.objects.all().count()

    #     return context