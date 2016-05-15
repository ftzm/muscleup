"""Serializers for Django Rest Framework"""

from rest_framework import serializers
from core.models import Exercise, Workout, Routine, RoutineDay, RoutineDaySlot
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

# Custom mixin for filtering related field querysets
class FilterRelatedMixin(object):
    def __init__(self, *args, **kwargs):
        super(FilterRelatedMixin, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, serializers.RelatedField):
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
        fields = ['url', 'id', 'name', 'owner']
        extra_kwargs = {
            'url': {'view_name': 'exercises-detail'}
            }

class RoutineDaySerializer(serializers.HyperlinkedModelSerializer):

    position = serializers.IntegerField()
    routine = serializers.HyperlinkedRelatedField(
        queryset = Routine.objects.all(),
        view_name='routines-detail'
    )

    class Meta:
        model = RoutineDay
        fields = ['id',
                  'name',
                  'position',
                  'routine']

class RoutineSerializer(serializers.HyperlinkedModelSerializer):
    cycle_length = serializers.IntegerField()
    cycle_position = serializers.IntegerField()
    routinedays = NestedHyperlinkedRelatedField(
        many=True,
        queryset = RoutineDay.objects.all(),
        view_name='routinedays-detail',
        parent_lookup_field = 'routine',
        parent_lookup_url_kwarg='routines_pk'
    )

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

