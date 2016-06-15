"""
forms
"""

from django import forms
from core.models import Exercise
from core.models import RoutineDay

class ExerciseForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    bodyweight = forms.BooleanField(label='bodyweight', required=False)

    def create_record(self, user):
        name = self.cleaned_data['name']
        bodyweight = self.cleaned_data['bodyweight']
        Exercise.objects.create(owner=user, name=name, bodyweight=bodyweight)

class RoutineDaySlotForm(forms.Form):
    exercise = forms.IntegerField(label='exercise')
    routineday = forms.IntegerField(label='Routine Day')

    def create_record(self, user):
        exercise = self.cleaned_data['exercise']
        routineday = self.cleaned_data['routineday']
        RoutineDay.objects.create(owner=user, routineday=routineday,
                                  exercise=exercise)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
