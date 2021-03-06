"""
functions for processing sets into data for progress charts
"""
from datetime import datetime, timezone
import json
from core.models import Exercise

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

def group_same_weight_neighbors(data):
    # sort into sublist of consecutive same weights
    consecutive_same_weights = []
    dbin = []
    for d in data:
        if not dbin or d['y'] == dbin[-1]['y']:
            dbin.append(d)
        else:
            consecutive_same_weights.append(dbin)
            dbin = [d]
    consecutive_same_weights.append(dbin)
    return consecutive_same_weights

def calculate_marker_sizes(data):
    dbins = group_same_weight_neighbors(data)

    # add  marker size calculated based on number of reps
    # relative to others in dbin
    for dbin in dbins:
        dbin_reps = [d['reps'] for d in dbin]
        lowest = min(dbin_reps)
        highest = max(dbin_reps) - lowest
        min_size = 4
        max_enlarge = 10
        for d in dbin:
            radius = min_size + ((d['reps'] - lowest) / highest) * max_enlarge
            d['marker']['radius'] = radius

    # return flattened list
    return [d for dbin in dbins for d in dbin]

def process_bodyweight_data(sets):
    assessed_sets = {}
    data = []
    for set in sets:
        date = dt_date_to_epoch(set.workout.date)
        try:
            assessed_sets[date] += set.reps
        except KeyError:
            assessed_sets[date] = set.reps
    for k, v in assessed_sets.items():
        data.append({"x":k, "y":v, "marker":{"symbol":"circle"}})
    return data

def process_weighted_data(sets):
    assessed_sets = {}
    data = []
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
        data.append({"x":k, "y":v1, "marker":{"symbol":"circle"}, "reps":v2})

    data = calculate_marker_sizes(data)
    return data

def get_chart_data(pks):
    output = []
    exercises = get_exercises(pks)
    for exercise in exercises:
        sets = exercise.sets.all()
        if not sets:
            continue
        if exercise.bodyweight is True:
            scale = 'reps'
            yaxis = 1
            pointformat = 'reps: <b>{point.y}</b>'
            data = process_bodyweight_data(sets)
        else:
            scale = 'lbs'
            yaxis = 0
            pointformat = 'weight: <b>{point.y} </b>, reps: <b>{point.reps}</b>'
            data = process_weighted_data(sets)

        output.append({
            "name":exercise.name,
            "yAxis":yaxis,
            "tooltip": {"pointFormat":pointformat},
            "data":data})

    return json.dumps(output)
