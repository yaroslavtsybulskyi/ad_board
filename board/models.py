from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count
from django.utils.timezone import now


def validate_price(value: Decimal) -> None:
    """
    Custom validator to ensure the price is a positive number.
    Raises a ValidationError if the value is not a number or less than or equal to 0.
    :param value: value to validate
    :return: None
    """
    if not isinstance(value, (int, Decimal)):
        raise ValidationError('Invalid price: must be a number.')
    if value <= 0:
        raise ValidationError('Price must be greater than 0')


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional user information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        """
        String representation of the user profile.
        """
        return self.user.username


class Category(models.Model):
    """
    Represents a category for ads (e.g., Electronics, Cars, Jobs).
    """

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)

    def active_ads_count(self) -> int:
        """
        Returns the number of active ads in this category.
        """
        return self.ads.filter(is_active=True).count()

    def __str__(self) -> str:
        """
        String representation of the category.
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Ad(models.Model):
    """
    Represents a classified ad posted by a user.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[validate_price])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    image = models.ImageField(upload_to='ads/', blank=True, null=True)

    def short_description(self) -> str:
        """
        Returns a shortened version of the ad description (max 100 characters).
        """
        return self.description[:100] if len(self.description) > 100 else self.description

    @classmethod
    def deactivate_old_ads(cls) -> None:
        """
        Deactivates ads that are older than 30 days and still marked as active.
        """
        expired_ads = cls.objects.filter(created_at__lt=now() - timedelta(days=30), is_active=True)
        for ad in expired_ads:
            ad.is_active = False
            ad.save()

    @classmethod
    def get_ads_last_month(cls):
        """
        Returns all ads created within the last 30 days.
        """
        return cls.objects.filter(created_at__gte=now() - timedelta(days=30))

    @classmethod
    def get_active_ads_in_category(cls, category):
        """
        Returns all active ads in the given category (by name).
        :param category: category to get active ads for
        """
        return cls.objects.filter(category__name=category).filter(is_active=True)

    @classmethod
    def get_ads_with_comments_count(cls):
        """
        Returns all ads with an additional annotation of the number of comments each ad has.
        """
        return cls.objects.annotate(comments_count=Count('comments'))

    @classmethod
    def get_user_ads(cls, user):
        """
        Returns all active ads created by the given user (UserProfile instance).
        """
        return cls.objects.filter(user=user).filter(is_active=True)

    def __str__(self):
        """
        String representation of the ad.
        """
        return f"{self.title}: {self.price}"


class Comment(models.Model):
    """
    Represents a comment left by a user on an ad.
    """

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def total_comments(self):
        """
        Represents a comment left by a user on an ad.
        """
        return self.ad.comments.count()

    def __str__(self):
        """
        String representation of the comment.
        """
        return f"Comment by {self.user.username} on {self.ad.title}"
