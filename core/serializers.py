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
    """
    mixin that filters all related fields by the current user
    """

    def __init__(self, *args, **kwargs):
        super(FilterUserRelatedMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, serializers.RelatedField):
                try:
                    request = self.context['request']
                    field.queryset = field.queryset.filter(owner=request.user)
                except AttributeError:
                    pass

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
    parent_name = None

    # Override internal method to disable use of PKOnlyObject which
    # so get_url() can access actual instance attributes
    def use_pk_only_optimization(self):
        return False

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.parent_name + '_pk': getattr(obj, self.parent_name).pk,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs,
                       request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            self.parent_name + '__pk': view_kwargs[self.parent_name + 'pk'],
            'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)

class TripleHyperlink(serializers.HyperlinkedRelatedField):
    """
    Class to simplify hyperlinks to once-nested resources.
    Supply the view name, the grandparent resource and
    the parent resource.

    Requires that:
    'pk' be used as the lookup field for all models,
    the nested url kwarg be 'pk',
    the parent url kwarg have the format 'parentname_pk',
    the nested model foreignkey field to parent be the same parentname
        as in the url.

    """
    grandparent_name = None
    parent_name = None

    # Override internal method to disable use of PKOnlyObject which
    # so get_url() can access actual instance attributes
    def use_pk_only_optimization(self):
        return False

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.grandparent_name + '_pk': getattr(getattr(
                obj, self.parent_name), self.grandparent_name).pk,
            self.parent_name + '_pk': getattr(obj, self.parent_name).pk,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs,
                       request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            self.grandparent_name + "__" + self.parent_name ++ '__pk': \
                view_kwargs[self.parent_name + 'pk'],
            self.parent_name + '__pk': view_kwargs[self.parent_name + 'pk'],
            'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)

class WorkoutSetHyperlink(DoubleHyperlink):
    view_name = 'workouts-sets-detail'
    parent_name = 'workout'

class ExerciseSetHyperlink(DoubleHyperlink):
    view_name = 'exercises-sets-detail'
    parent_name = 'exercise'

class RoutineDayHyperlink(DoubleHyperlink):
    view_name = 'routines-routinedays-detail'
    parent_name = 'routine'

class RoutineDaySlotHyperlink(TripleHyperlink):
    view_name = 'routines-routinedays-slot-detail'
    grandparent_name = 'routine'
    parent_name = 'routineday'

class ExerciseSerializer(serializers.ModelSerializer):
    sets = ExerciseSetHyperlink(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ['url',
                  'id',
                  'name',
                  'sets',
                 ]
        extra_kwargs = {
            'url': {'view_name': 'exercises-detail'}
            }

class RoutineDaySlotSerializer(FilterUserRelatedMixin,
                               serializers.ModelSerializer):

    exercise = serializers.HyperlinkedRelatedField(
        view_name='exercises-detail',
        queryset=Exercise.objects.all())
    progression = serializers.HyperlinkedRelatedField(
        view_name='progressions-detail',
        queryset=Progression.objects.all())
    routineday = RoutineDayHyperlink(queryset=RoutineDay.objects.all())

    class Meta:
        model = RoutineDaySlot
        fields = ['id',
                  'exercise',
                  'routineday',
                  'order',
                  'progression',
                  # 'upgrade',
                  'main_reps_goal',
                  'main_weight_goal',
                  'main_sets_goal',
                  'snd_reps_goal',
                  'snd_weight_goal',
                  'snd_sets_goal'
                 ]


class RoutineDaySerializer(FilterUserRelatedMixin,
                           serializers.HyperlinkedModelSerializer):

    position = serializers.IntegerField()
    routine = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='routines-detail'
    )
    routinedayslots = RoutineDaySlotHyperlink(many=True, read_only=True)

    class Meta:
        model = RoutineDay
        fields = ['id',
                  'name',
                  'position',
                  'routinedayslots',
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
    sets = WorkoutSetHyperlink(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ['url',
                  'id',
                  'name',
                  'date',
                  'routineday',
                  'sets',
                 ]
        extra_kwargs = {
            'url': {'view_name': 'workouts-detail'}
            }

    def create(self, validated_data):
        return Workout.objects.create_workout(**validated_data)

    def filter_routineday(self, queryset):
        request = self.context['request']
        return queryset.filter(owner=request.user)

class ProgressionSlotHyperlink(DoubleHyperlink):
    view_name = 'progressions-progressionslots-detail'
    parent_name = 'progression'

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
        serializer_url_field = WorkoutSetHyperlink
        model = Set
        fields = ['id', 'exercise', 'reps', 'weight']

class ExerciseSetSerializer(FilterUserRelatedMixin, serializers.ModelSerializer):
    workout = serializers.HyperlinkedRelatedField(
        queryset=Workout.objects.all(),
        view_name='workouts-detail',
        )

    class Meta:
        serializer_url_field = ExerciseSetHyperlink
        model = Set
        fields = ['id', 'workout', 'reps', 'weight']
