"""models for muscleup core"""

import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class MuscleupUserManager(BaseUserManager):

    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        self.create_user(email, password)


class MuscleupUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nick = models.CharField(max_length=30, default="Champ")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_active(self):
        return True

    @property
    def get_full_name(self):
        return self.name

    @property
    def get_short_name(self):
        return self.name

    objects = MuscleupUserManager()


class Exercise(models.Model):
    name = models.TextField(default="", unique=True)
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='exercises')
    bodyweight = models.BooleanField(default=False)

    def __str__(self):
        return 'Exercise: "{}"'.format(self.name)


class Routine(models.Model):
    """TODO: field explanations"""
    name = models.TextField(default="")
    _cycle_length = models.IntegerField(
        default=1, db_column="cycle_length")
    _cycle_position = models.IntegerField(
        default=1, db_column="cycle_position")
    cycle_last_set = models.DateField(default=timezone.now)
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='routines')
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Routine "{}"'.format(self.name)

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


class Progression(models.Model):
    name = models.TextField(default="")
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='progressions')

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

    @property
    def current(self):
        return self.progressionslots.filter(_current=True).first().exercise


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
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='progressionslots')

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


class RoutineDay(models.Model):
    """
    Model representing a day in a fitness routine.
    """

    name = models.TextField(default="")
    routine = models.ForeignKey(
        Routine, default=1, on_delete=models.CASCADE,
        related_name='routinedays')
    _position = models.IntegerField(
        default=1, db_column="position")
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='routinedays')

    def __str__(self):
        return 'RoutineDay "{}"'.format(self.name)

    @property
    def exercises(self):
        return [s.exercise for s in self.routinedayslots.all()]

    @property
    def available_exercises(self):
        return [e for e in self.owner.exercises.all()
                if e not in self.exercises]

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


class Upgrade(models.Model):
    name = models.TextField()
    main_reps_adj = models.IntegerField(default=0)
    main_weight_adj = models.IntegerField(default=0)
    main_sets_adj = models.IntegerField(default=0)
    snd_reps_adj = models.IntegerField(default=0)
    snd_weight_adj = models.IntegerField(default=0)
    snd_sets_adj = models.IntegerField(default=0)
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='upgrades')


class RoutineDaySlot(models.Model):
    """
    relationship model between routineday and exercise,
    exists for ordering
    """

    exercise = models.ForeignKey(
        Exercise, default=1, on_delete=models.CASCADE,
        related_name='routinedayslots', db_column="exercise")
    routineday = models.ForeignKey(
        RoutineDay, default=1, on_delete=models.CASCADE,
        db_column='routineday',
        related_name='routinedayslots')
    _order = models.IntegerField(default=0, db_column="order")
    progression = models.ForeignKey(
        Progression, null=True, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(
        Upgrade, null=True)
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='routinedayslots')

    reps_min = models.IntegerField(default=0)
    reps_max = models.IntegerField(default=0)
    reps_step = models.IntegerField(default=0)
    sets_min = models.IntegerField(default=0)
    sets_max = models.IntegerField(default=0)
    weight_step = models.IntegerField(default=0)

    fail_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('exercise', 'routineday')

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

    def apply_order(self):
        peer_count = len(self.routineday.routinedayslots.all())
        if self._order == 0:
            self._order = peer_count + 1

class WorkoutManager(models.Manager):  # pylint: disable=too-few-public-methods
    def create_workout(self,
                       routineday=None,
                       owner=None,
                       date=None,
                       name=None,
                       ):
        if name is None:
            if routineday is not None:
                previous = Workout.objects.filter(
                    routineday=routineday).count()
                name = "{} - {} - {}".format(
                    routineday.routine.name, routineday.name, previous+1)
            else:
                previous = Workout.objects.filter(
                    routineday__isnull=True).count()
                name = "Untitled - {}".format(previous+1)
        if date is None:
            date = datetime.date.today()

        workout = self.create(
            routineday=routineday, name=name, date=date, owner=owner)
        return workout


class Workout(models.Model):
    name = models.TextField(default='')
    date = models.DateField(default=datetime.date.today)
    routineday = models.ForeignKey(
        RoutineDay, null=True, on_delete=models.CASCADE,
        related_name='workouts')
    owner = models.ForeignKey(MuscleupUser,
                              default=1,
                              on_delete=models.CASCADE,
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
    owner = models.ForeignKey(MuscleupUser, default=1,
                              on_delete=models.CASCADE,
                              related_name='sets')
