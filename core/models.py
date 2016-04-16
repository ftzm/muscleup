"""models for muscleup core"""

import datetime
from django.db import models
from django.utils import timezone


class Exercise(models.Model):
    name = models.TextField(default="")


class Routine(models.Model):
    """TODO: field explanations"""
    name = models.TextField(default="")
    _cycle_length = models.IntegerField(
        default=1, db_column="cycle_length")
    _cycle_position = models.IntegerField(
        default=1, db_column="cycle_position")
    cycle_last_set = models.DateField(default=timezone.now)

    def update_cycle_position(self):
        self.cycle_position = self.cycle_position + \
            (datetime.date.today() - self.cycle_last_set).days \
            % self.cycle_length

    @property
    def cycle_length(self):
        return self._cycle_length

    @cycle_length.setter
    def cycle_length(self, num):
        self._cycle_length = num
        for routineday in self.routinedays.all():
            if routineday.position > num:
                routineday.position = num
                routineday.save()
        if self.cycle_position > num:
            self.cycle_position = num

    @property
    def cycle_position(self):
        return self._cycle_position

    @cycle_position.setter
    def cycle_position(self, num):
        if 0 < num <= self.cycle_length:
            self._cycle_position = num
        else:
            pass
        self.cycle_last_set = datetime.date.today()


class RoutineDay(models.Model):
    name = models.TextField(default="")
    routine = models.ForeignKey(
        Routine, default=1, on_delete=models.CASCADE,
        related_name='routinedays')
    _position = models.IntegerField(
        default=1, db_column="position")

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, num):
        if 0 < num <= self.routine.cycle_length:
            self._position = num
        else:
            pass
            # todo: handle this somehow

    def add_exercise(self, exercise):
        RoutineDaySlot.objects.create(
            routineday=self, exercise=exercise)

    def remove_exercise(self, name):
        routinedayslot = self.routinedayslots.filter(exercise__name=name)
        if routinedayslot:
            routinedayslot.delete()

    def close_gap(self, gap):
        for slot in self.routinedayslots.all():
            if slot.order > gap:
                slot._order -= 1
                slot.save()


class RoutineDaySlot(models.Model):
    """
    relationship model between routineday and exercise,
    exists for ordering
    """
    exercise = models.ForeignKey(
        Exercise, default=1, on_delete=models.CASCADE,
        related_name='routinedayslots')
    _routineday = models.ForeignKey(
        RoutineDay, default=1, on_delete=models.CASCADE,
        db_column='routineday',
        related_name='routinedayslots')
    _order = models.IntegerField(default=1, db_column="order")

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, new_order):
        other_slots = self.routineday.routinedayslots.all()
        old_order = self._order
        if new_order > old_order:
            middle_slots = [s for s in other_slots
                            if old_order < s.order <= new_order]
            for slot in middle_slots:
                slot._order -= 1
                slot.save()
        elif new_order < old_order:
            middle_slots = [s for s in other_slots
                            if old_order > s.order >= new_order]
            for slot in middle_slots:
                slot._order += 1
                slot.save()
        self._order = new_order

    @property
    def routineday(self):
        return self._routineday

    @routineday.setter
    def routineday(self, routineday):
        try:
            self._order = 1 + \
                max([r.order for r in routineday.routinedayslots.all()])
        except ValueError:
            pass
        self._routineday = routineday


class WorkoutManager(models.Manager): #pylint: disable=too-few-public-methods
    def create_workout(self, routineday=None):
        if routineday is not None:
            previous = Workout.objects.filter(routineday=routineday).count()
            name = "{} - {} - {}".format(
                routineday.routine.name, routineday.name, previous+1)
        else:
            previous = Workout.objects.filter(routineday__isnull=True).count()
            name = "Untitled - {}".format(previous+1)
        workout = self.create(routineday=routineday, name=name)
        return workout


class Workout(models.Model):
    name = models.TextField(default='')
    date = models.DateField(default=datetime.date.today)
    routineday = models.ForeignKey(
        RoutineDay, null=True, on_delete=models.CASCADE,
        related_name='workouts')

    objects = WorkoutManager()

class Set(models.Model):
    exercise = models.ForeignKey(
        Exercise, default=1, on_delete=models.CASCADE,
        related_name='sets')
    reps = models.IntegerField(default=1)
    weight = models.IntegerField(null=True)
    workout = models.ForeignKey(
        Workout, default=1, on_delete=models.CASCADE,
        related_name='sets')


class Progression(models.Model):
    name = models.TextField(default="", unique=True)

    def add_exercise(self, exercise):
        ProgressionSlot.objects.create(
            progression=self, exercise=exercise)

    def remove_exercise(self, name):
        progressionslot = self.progressionslots.filter(exercise__name=name)
        if progressionslot:
            progressionslot.delete()

    def close_gap(self, gap):
        for slot in self.progressionslots.all():
            if slot.order > gap:
                slot._order -= 1
                slot.save()


class ProgressionSlot(models.Model):
    """
    Relationship object between progressions and exercises.
    For ordering and maybe more later.
    """
    exercise = models.ForeignKey(
        Exercise, default=1, on_delete=models.CASCADE,
        related_name='progressionslots')
    _progression = models.ForeignKey(
        Progression, default=1, on_delete=models.CASCADE,
        related_name='progressionslots',
        db_column="progression")
    _order = models.IntegerField(default=1, db_column="order")
    _current = models.BooleanField(default=False, db_column="current")

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, new_order):
        other_slots = self.progression.progressionslots.all()
        old_order = self._order
        if new_order > old_order:
            middle_slots = [s for s in other_slots
                            if old_order < s.order <= new_order]
            for slot in middle_slots:
                slot._order -= 1
                slot.save()
        elif new_order < old_order:
            middle_slots = [s for s in other_slots
                            if old_order > s.order >= new_order]
            for slot in middle_slots:
                slot._order += 1
                slot.save()
        self._order = new_order

    @property
    def progression(self):
        return self._progression

    @progression.setter
    def progression(self, progression):
        try:
            self._order = 1 + \
                max([r.order for r in progression.progressionslots.all()])
        except ValueError:
            pass
        self._progression = progression

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        if value is False:
            self._current = False
        else:
            previous = self.progression.progressionslots.filter(
                _current=True).first()
            if previous:
                previous.current = False
                previous.save()
            self._current = value
