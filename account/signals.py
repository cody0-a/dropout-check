from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DropOut, DropoutSummary

@receiver(post_save, sender=DropOut)
def update_dropout_summary(sender, instance, created, **kwargs):
    if created:
        summary, _ = DropoutSummary.objects.get_or_create(id=1)
        summary.total_dropouts += 1

        if instance.DropOut_case == "Academic":
            summary.academic_dropouts += 1
        elif instance.DropOut_case == "Financial":
            summary.financial_dropouts += 1
        elif instance.DropOut_case == "Health":
            summary.health_dropouts += 1
        elif instance.DropOut_case == "Personal":
            summary.personal_dropouts += 1
        elif instance.DropOut_case == "Marriage":
            summary.marriage_dropouts += 1
        elif instance.DropOut_case == "Distance":
            summary.distance_dropouts += 1
        elif instance.DropOut_case == "Death":
            summary.death_dropouts += 1
        else:
            summary.other_dropouts += 1

        summary.save()