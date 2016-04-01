"""database signals"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
from core.models import RoutineDaySlot
from core.models import ProgressionSlot


@receiver(post_delete, sender=RoutineDaySlot)
def trigger_routinedayslot_gapclose(**kwargs):
    instance = kwargs['instance']
    instance.routineday.close_gap(instance.order)


@receiver(post_delete, sender=ProgressionSlot)
def trigger_progressionslot_gapclose(**kwargs):
    instance = kwargs['instance']
    instance.progression.close_gap(instance.order)
