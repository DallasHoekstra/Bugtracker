# signal that triggers after a model is saved
from django.db.models.signals import post_save
# user will be the sender (of the signal)
from django.contrib.auth.models import User
# receiver will be the receiver of the signal and will do something based on the signal
from django.dispatch import receiver

from .models import Profile

# Creates a profile page for a user when the user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()