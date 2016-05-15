"""Serializers for Django Rest Framework"""

from rest_framework import serializers
from core.models import Exercise, Workout, Routine, RoutineDay, RoutineDaySlot


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


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ['url', 'id', 'name']
        extra_kwargs = {
            'url': {'view_name': 'exercises-detail'}
            }

class RoutineSerializer(serializers.HyperlinkedModelSerializer):
    cycle_length = serializers.IntegerField()
    cycle_position = serializers.IntegerField()

    class Meta:
        model = Routine
        fields = ['url', 'name', 'cycle_length', 'cycle_position',
                  'cycle_last_set']
        extra_kwargs = {
            'url': {'view_name': 'routines-detail'}
            }

class RoutineDaySerializer(FilterRelatedMixin, serializers.HyperlinkedModelSerializer):

    position = serializers.IntegerField()
    routine = serializers.HyperlinkedRelatedField(
        view_name='routines-detail',
        queryset=Routine.objects.all()
        )

    class Meta:
        model = RoutineDay
        fields = ['name', 'routine', 'position']

    def filter_routine(self, queryset):
        request = self.context['request']
        return queryset.filter(owner=request.user)
