from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from board.models import Ad


@receiver(post_save, sender=Ad)
def check_ad_expiry(sender, instance, **kwargs):
    """
    Signal handler that runs after any Ad is saved.
    """
    Ad.deactivate_old_ads()


@receiver(post_save, sender=Ad)
def send_ad_creation_email(sender, instance, created, **kwargs):
    """
    Signal handler that runs after an Ad is created.
    """
    if created:
        subject = 'Ad Created Successfully!'
        message = f"Dear {instance.user.user.username},\n\nYour ad '{instance.title}' has been successfully posted!"

        send_mail(subject, message, "admin@board.com",
                  [instance.user.email], fail_silently=False)
