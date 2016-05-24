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
    MuscleupUser,
    Set,
    )

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

class FilterUserRelatedMixin(object):

    def __init__(self, *args, **kwargs):
        super(FilterUserRelatedMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, serializers.RelatedField):
                try:
                    request = self.context['request']
                    field.queryset = field.queryset.filter(owner=request.user)
                except AttributeError:
                    pass

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['url',
                  'id',
                  'name',
                 ]
        extra_kwargs = {
            'url': {'view_name': 'exercises-detail'}
            }

class DoubleHyperlink(serializers.HyperlinkedRelatedField):
    """
    Class to simplify hyperlinks to once-nested resources.
    Supply the view name and name of the parent resource.

    Requires that:
    'pk' be used as the lookup field for all models,
    the nested url kwarg be 'pk',
    the parent url kwarg have the format 'parentname_pk',
    the nested model foreignkey field to parent be the same parentname
        as in the url.

    """
    top_name = None

    # Override internal method to disable use of PKOnlyObject which
    # so get_url() can access actual instance attributes
    def use_pk_only_optimization(self):
        return False

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.top_name + '_pk': getattr(obj, self.top_name).pk,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs,
                       request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            self.top_name + '__pk': view_kwargs[self.top_name + 'pk'],
            'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)

class RoutineDayHyperlink(DoubleHyperlink):
    view_name = 'routines-routinedays-detail'
    top_name = 'routine'

class RoutineDaySerializer(FilterUserRelatedMixin,
                           serializers.HyperlinkedModelSerializer):

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

class RoutineSerializer(FilterUserRelatedMixin, serializers.HyperlinkedModelSerializer):
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

class WorkoutSerializer(FilterUserRelatedMixin, serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
    routineday = RoutineDayHyperlink(queryset=RoutineDay.objects.all())

    class Meta:
        model = Exercise
        fields = ['url',
                  'id',
                  'name',
                  'date',
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

class ProgressionSerializer(FilterUserRelatedMixin,
                            serializers.ModelSerializer):

    progressionslots = ProgressionSlotHyperlink(many=True, read_only=True)

    class Meta:
        model = Progression
        fields = ('url', 'id', 'name', 'progressionslots')
        extra_kwargs = {
            'url': {'view_name': 'progressions-detail'}
            }

class ProgressionSlotSerializer(FilterUserRelatedMixin,
                                serializers.ModelSerializer):
    _progression = serializers.PrimaryKeyRelatedField(
        read_only=True)
    exercise = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        )

    class Meta:
        model = ProgressionSlot
        fields = ['id', 'exercise', '_progression']

class SetSerializer(FilterUserRelatedMixin, serializers.ModelSerializer):
    exercise = serializers.HyperlinkedRelatedField(
        queryset=Exercise.objects.all(),
        view_name='exercises-detail',
        )
    workout = serializers.HyperlinkedRelatedField(
        queryset=Workout.objects.all(),
        view_name='workouts-detail',
        )

    class Meta:
        model = Set
        fields = ['id', 'url', 'exercise', 'workout', 'reps', 'weight']
        extra_kwargs = {
            'url': {'view_name': 'sets-detail'}
            }

class WorkoutSetSerializer(FilterUserRelatedMixin, serializers.ModelSerializer):
    exercise = serializers.HyperlinkedRelatedField(
        queryset=Exercise.objects.all(),
        view_name='exercises-detail',
        )

    class Meta:
        model = Set
        fields = ['id', 'exercise', 'reps', 'weight']
        extra_kwargs = {
            'url': {'view_name': 'workouts-sets-detail'}
            }
