from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Imc, WeightHistory


@receiver(post_save, sender=WeightHistory)
def save_imc(sender, instance, **kwargs):
    Imc.objects.filter(user_id=instance.user.id).update(
        current_weight=instance.weight)


@receiver(post_save, sender=Imc)
def create_weight_history(sender, instance, created, **kwargs):
    current_weight = WeightHistory.objects.filter(
        user=instance.user).order_by('-created_at').first()
    if current_weight and \
        current_weight.weight != instance.current_weight:
        WeightHistory.objects.create(
            weight=instance.current_weight,
            user=instance.user,
        )

