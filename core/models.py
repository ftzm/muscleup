"""models for muscleup core"""

import datetime
from django.db import models


class Exercise(models.Model):
    name = models.TextField(default="")


class Routine(models.Model):
    name = models.TextField(default="")
    _cycle_length = models.IntegerField(
        default=1, db_column="cycle_length")
    _cycle_position = models.IntegerField(
        default=1, db_column="cycle_position")

    # update_cycle_position
    """
         if datetime.date.today() == self.cycle_position_set:
            return
        try:
            delta = datetime.date.today() - self.cycle_position_set
        except:
            return
        shift = delta.days % self.cycle_length
        new_position = self.cycle_position + shift
        if new_position > self.cycle_length:
            new_position = new_position - self.cycle_length
        self.cycle_position = new_position
        self.cycle_position_set = datetime.date.today()
        """

    @property
    def cycle_length(self):
        return self._cycle_length

    @cycle_length.setter
    def cycle_length(self, num):
        self._cycle_length = num

    @property
    def cycle_position(self):
        return self._cycle_position

    @cycle_position.setter
    def cycle_position(self, num):
        self._cycle_position = num


class RoutineDay(models.Model):
    name = models.TextField(default="")
    next_date = models.DateField(default=datetime.date.today)

    #


class RoutineDaySlot(models.Model):
    pass


class Workout(models.Model):
    name = models.TextField(default='')
    date = models.DateField(default=datetime.date.today)


class Set(models.Model):
    exercise = models.ForeignKey(
        Exercise, default=1, on_delete=models.CASCADE,
        related_name='sets')
    reps = models.IntegerField(default=1)
    weight = models.IntegerField(null=True)
    workout = models.ForeignKey(
        Workout, default=1, on_delete=models.CASCADE,
        related_name='sets')
