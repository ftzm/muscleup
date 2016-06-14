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
from core.models import (
    Exercise,
    Routine,
    RoutineDay,
    RoutineDaySlot,
    )
from core.chart import get_chart_data
from core.forms import ContactForm

class BaseView(View):
    context = {}
    context['urls'] = [('progress', 'Progress'),
                       ('routines', 'Routines'),
                       ('exercises', 'Exercises')]
    def logged_in(self, context):
        context['logged_in'] = self.request.user.is_authenticated()
        return context


class Home(BaseView):
    def get(self, request):
        self.context = self.logged_in(self.context)
        if self.context['logged_in'] is True:
            self.context['name'] = 'Champ'
        else:
            self.context['name'] = 'Stranger'
        return render(request, 'core/home.html', self.context)

class Login(BaseView):
    def get(self, request):
        self.context['next'] = request.GET.get('next', '')
        return render(request, 'core/login.html', self.context)

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
        self.context['exercises'] = Exercise.objects.filter(owner=request.user)
        return render(request, 'core/exercises.html', self.context)

    def post(self, request):
        name = request.POST['name']
        bodyweight = request.POST.get('bodyweight', False)
        Exercise.objects.create(name=name, bodyweight=bodyweight, owner=request.user)
        return HttpResponseRedirect('/exercises')

@method_decorator(login_required, name='dispatch')
class DeleteExercise(BaseView):
    def get(self, request, pk):
        exercise = Exercise.objects.get(pk=pk, owner=request.user)
        if exercise:
            exercise.delete()
        return HttpResponseRedirect('/exercises/')

class Routines(BaseView):
    def get(self, request):
        self.context = self.logged_in(self.context)
        self.context['routines'] = Routine.objects.filter(owner=request.user)
        self.context['msg'] = request.GET.get('msg', '')
        return render(request, 'core/routines.html', self.context)

    def post(self, request):
        name = request.POST['name']
        length = int(request.POST.get('length', False))
        position = int(request.POST.get('position', False))
        Routine.objects.create(name=name, cycle_length=length, cycle_position=position)
        return HttpResponseRedirect('/routines')

@method_decorator(login_required, name='dispatch')
class DeleteRoutine(BaseView):
    def get(self, request, pk):
        routine = Routine.objects.get(pk=pk, owner=request.user)
        if routine:
            routine.delete()
        return HttpResponseRedirect('/routines/')

@method_decorator(login_required, name='dispatch')
class AddRoutinedayslot(BaseView):
    def post(self, request):
        exercise_id = int(request.POST.get('exercise', False))
        exercise = Exercise.objects.get(pk=exercise_id)
        routineday_id = int(request.POST.get('routineday', False))
        routineday = RoutineDay.objects.get(pk=routineday_id)
        if exercise and routineday:
            try:
                RoutineDaySlot.objects.create(routineday=routineday,
                                              exercise=exercise,
                                              owner=request.user)
                return HttpResponseRedirect('/routines/')
            except:
                msg = "failed to schedule exercise"
                return HttpResponseRedirect('/routines/?msg={}'.format(msg))

@method_decorator(login_required, name='dispatch')
class DeleteRoutinedayslot(BaseView):
    def get(self, request, pk):
        routinedayslot = RoutineDaySlot.objects.get(pk=pk, owner=request.user)
        if routinedayslot:
            routinedayslot.delete()
        return HttpResponseRedirect('/routines/')
