from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from network.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user=kwargs['instance']
        profile = Profile.objects.create(person=user)
        # profile.following.set([user.id])
        profile.save()