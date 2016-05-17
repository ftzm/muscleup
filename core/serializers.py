"""Serializers for Django Rest Framework"""

from rest_framework import serializers
from rest_framework.reverse import reverse
from core.models import (
    Exercise,
    Workout,
    Routine,
    RoutineDay,
    RoutineDaySlot,
    Progression,
    ProgressionSlot,
    MuscleupUser
    )
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

class FilterRelatedMixin(object):
    """
    Custom mixin for filtering related field querysets.
    Used in conjunction with a function like this:

    def filter_routineday(self, queryset):
        request = self.context['request']
        return queryset.filter(owner=request.user)

    where "routineday" matches the name of the field to be filtered.

    """
    def __init__(self, *args, **kwargs):
        super(FilterRelatedMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, serializers.RelatedField) or \
                isinstance(field, NestedHyperlinkedRelatedField):
                method_name = 'filter_%s' % name
                try:
                    func = getattr(self, method_name)
                except AttributeError:
                    pass
                else:
                    field.queryset = func(field.queryset)


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['url',
                  'id',
                  'name',
                  'owner'
                 ]
        extra_kwargs = {
            'url': {'view_name': 'exercises-detail'}
            }

class RoutineDayHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'routines-routinedays-detail'

    # Override internal method to disable use of PKOnlyObject which
    # so get_url() can access actual instance attributes
    def use_pk_only_optimization(self):
        return False

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'routine_pk': obj.routine.pk,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'routine__pk': view_kwargs['routine_pk'],
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)

class RoutineDaySerializer(serializers.HyperlinkedModelSerializer):

    position = serializers.IntegerField()
    routine = serializers.HyperlinkedRelatedField(
         read_only=True,
         view_name='routines-detail'
    )

    class Meta:
        model = RoutineDay
        fields = ['id',
                  'name',
                  'position',
                  'routine'
                 ]

class RoutineSerializer(serializers.HyperlinkedModelSerializer):
    cycle_length = serializers.IntegerField()
    cycle_position = serializers.IntegerField()
    routinedays = RoutineDayHyperlink(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = ['url',
                  'id',
                  'name',
                  'cycle_length',
                  'cycle_position',
                  'cycle_last_set',
                  'routinedays'
                 ]
        extra_kwargs = {
            'url': {'view_name': 'routines-detail'}
            }

class WorkoutSerializer(FilterRelatedMixin, serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
    owner = serializers.PrimaryKeyRelatedField(
        queryset = MuscleupUser.objects.all())
    routineday = RoutineDayHyperlink(queryset=RoutineDay.objects.all())

    class Meta:
        model = Exercise
        fields = ['url',
                  'id',
                  'name',
                  'date',
                  'owner',
                  'routineday'
                 ]
        extra_kwargs = {
            'url': {'view_name': 'workouts-detail'}
            }

    def create(self, validated_data):
        return Workout.objects.create_workout(**validated_data)

    def filter_routineday(self, queryset):
        request = self.context['request']
        return queryset.filter(owner=request.user)

class ProgressionSlotHyperlink(serializers.HyperlinkedRelatedField):
    view_name = 'progressions-progressionslots-detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'progression_pk': obj.progression.pk,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'progression__pk': view_kwargs['progression_pk'],
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)

class ProgressionSerializer(serializers.ModelSerializer):

    progressionslots = ProgressionSlotHyperlink(many=True, read_only=True)

    class Meta:
        model = Progression
        fields=('url', 'id', 'name', 'progressionslots')
        extra_kwargs = {
            'url': {'view_name': 'progressions-detail'}
            }

class ProgressionSlotSerializer(serializers.ModelSerializer):
    _progression = serializers.PrimaryKeyRelatedField(
        read_only=True)
    exercise = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        )

    class Meta:
        model = ProgressionSlot
        fields = ['id', 'exercise', '_progression']

