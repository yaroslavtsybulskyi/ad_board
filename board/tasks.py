import logging

from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

logging = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_registrations_email(user_email: str) -> None:
    """
    Sends a registration confirmation email to a newly registered user.
    :param user_email: The email address of the user.
    :return: None
    """
    subject = "Registration Email"
    message = "Thank you for joining the Cult"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


@shared_task
def send_promo_email(user_email: str) -> None:
    """
    Sends a promotional email to the user.
    :param user_email: The email address of the user.
    :return: None
    """
    subject = "Discover new possibilities! Or not. It is up to you. Or not"
    message = "Become Christopher Columbus of nowadays! Explore our platform! Sell and be sold!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


@shared_task
def log_user_count() -> None:
    """
    Logs the current total number of users in the system.
    :return: None
    """
    user_count = User.objects.count()
    logging.info(f"User count: {user_count}")
