"""
Views for user facing website
"""
from django.shortcuts import render
from core.models import Exercise
from datetime import datetime, timezone
import json

def dt_date_to_epoch(date):
    dt = datetime.combine(date, datetime.min.time())
    epoch_second = dt.replace(tzinfo=timezone.utc).timestamp()
    epoch_milliseconds = epoch_second * 1000  # for javscript
    return int(epoch_milliseconds)

def get_exercises(pks):
    exercises = []
    for pk in pks:
        exercise = Exercise.objects.get(pk=pk)
        exercises.append(exercise)
    return exercises

def get_chart_data(pks):
    output = []
    exercises = get_exercises(pks)
    for exercise in exercises:
        assessed_sets = {}
        sets = exercise.sets.all()
        for set in sets:
            date = dt_date_to_epoch(set.workout.date)
            if set.weight == 0:
                try:
                    assessed_sets[date] += set.reps
                except KeyError:
                    assessed_sets[date] = set.reps
            else:
                try:
                    assessed_sets[date] = max(assessed_sets[date], set.weight)
                except KeyError:
                    assessed_sets[date] = set.weight
        data = []
        for k, v in assessed_sets.items():
            data.append([k, v])

        output.append({'name':exercise.name, 'data':json.dumps(data)})

    return output


def mockup(request):
    chart_data = get_chart_data([6])
    return render(request, 'core/mockup.html', {"chart_data":chart_data})
