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
        data = []
        if exercise.bodyweight is True:
            for set in sets:
                date = dt_date_to_epoch(set.workout.date)
                try:
                    assessed_sets[date] += set.reps
                except KeyError:
                    assessed_sets[date] = set.reps
            for k, v in assessed_sets.items():
                data.append([k, v])
        else:
            for set in sets:
                date = dt_date_to_epoch(set.workout.date)
                try:
                    weight, sets = assessed_sets[date]
                    if set.weight > weight:
                        assessed_sets[date] = (set.weight, set.reps)
                    elif set.weight == weight:
                        assessed_sets[date] = (set.weight,
                                               assessed_sets[date][1]+set.reps)
                    else:
                        pass
                except KeyError:
                    assessed_sets[date] = (set.weight, set.reps)
            for k, (v1, v2) in assessed_sets.items():
                data.append([k, v1, v2])
        output.append({
            'name':exercise.name,
            'bodyweight': exercise.bodyweight,
            'data':json.dumps(data)})

    return output


def mockup(request):
    chart_data = get_chart_data([6, 7])
    return render(request, 'core/mockup.html', {"chart_data":chart_data})
