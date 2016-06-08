#pylint:disable=no-self-use
"""
Views for user facing website
"""
import json
from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import *
from core.models import Exercise
from core.chart import get_chart_data
from core.forms import ContactForm

class BaseView(View):

    def logged_in(self, context):
        context['logged_in'] = self.request.user.is_authenticated()
        return context

    context = {}

class Home(BaseView):
    def get(self, request):
        self.context = self.logged_in(self.context)
        if self.context['logged_in'] is True:
            self.context['name'] = 'Champ'
        else:
            self.context['name'] = 'Stranger'
        return render(request, 'core/home.html', self.context)

class Login(View):
    def get(self, request):
        next = request.GET.get('next', '')
        return render(request, 'core/login.html', {'next':next})

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        next = request.POST.get('next', '')
        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)
            if next == "":
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/progress')

class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class Progress(BaseView):
    def get(self, request):
        self.context = self.logged_in(self.context)
        user = request.user
        all_exercise_pks = [e.pk for e in Exercise.objects.filter(owner=user)]
        self.context['chart_data'] = get_chart_data(all_exercise_pks)
        return render(request, 'core/progress.html', self.context)

@method_decorator(login_required, name='dispatch')
class Exercises(BaseView):
    def get(self, request):
        self.context = self.logged_in(self.context)
        user = request.user
        self.context['exercises'] = Exercise.objects.filter(owner=user)
        self.context['form'] = ContactForm
        return render(request, 'core/exercises.html', self.context)

    def post(self, request):
        name = request.POST['name']
        bodyweight = request.POST['bodyweight']
        Exercise.objects.create(name=name, bodyweight=bodyweight)
        return render(request, 'core/exercises.html', self.context)
