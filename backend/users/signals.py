from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.models import Student

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the user profile when a User instance is saved.
    """
    if instance.role == 'student':
        if created:
            Student.objects.create(user=instance)
        else:
            # Ensure the student profile exists
            Student.objects.get_or_create(user=instance)
