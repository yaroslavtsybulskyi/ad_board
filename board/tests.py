from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.test import TestCase

from board.models import UserProfile, Category, Ad, Comment


class ModelTest(TestCase):
    """
    Unit tests for models in the board app.
    """

    def setUp(self) -> None:
        """
        Prepare test data: create a user, profile, category,
        and two ads (one recent, one older than 30 days).
        """
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com')
        self.profile = UserProfile.objects.create(user=self.user, phone_number='+12312322222')

        self.category = Category.objects.create(name='Test', description='Test Description')

        self.ad = Ad.objects.create(
            title='Test Object',
            description='Test Description',
            price=500.00,
            user=self.profile,
            category=self.category,
            created_at=now() - timedelta(days=15),
            is_active=True
        )

        self.old_ad = Ad.objects.create(
            title="Old Test Object",
            description="Old Test Description",
            price=500.00,
            user=self.profile,
            category=self.category,
            is_active=False
        )

        self.old_ad.created_at = now() - timedelta(days=40)
        self.old_ad.save()

    def test_old_ads_deactivation(self) -> None:
        """
        Test that ads older than 30 days are automatically deactivated.
        """
        old_ad = Ad.objects.create(
            title="Old Laptop",
            description="An old laptop",
            price=200.00,
            user=self.profile,
            category=self.category,
            is_active=True
        )
        old_ad.created_at = now() - timedelta(days=31)
        old_ad.save()
        Ad.deactivate_old_ads()
        old_ad.refresh_from_db()

        self.assertFalse(old_ad.is_active, "Old ad should be deactivated")

    def test_price_validation(self) -> None:
        """
        Test that creating an ad with a negative price raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            ad = Ad(
                title="Old Laptop",
                description="An old laptop",
                price=-100.00,
                user=self.profile,
                category=self.category
            )
            ad.full_clean()

    def test_add_short_description(self) -> None:
        """
        Test that short_description() returns full string if short,
        and first 100 characters if long.
        """
        short_description = "Short Description"
        long_description = "test" * 50

        short_ad = Ad.objects.create(
            title="Old Laptop",
            description=short_description,
            price=200.00,
            user=self.profile,
            category=self.category,
        )

        long_ad = Ad.objects.create(
            title="Old Laptop",
            description=long_description,
            price=200.00,
            user=self.profile,
            category=self.category,
        )

        self.assertEqual(short_ad.short_description(), short_description)
        self.assertEqual(long_ad.short_description(), long_description[:100])

    def test_count_ad_comments(self) -> None:
        """
        Test that an ad returns the correct number of associated comments.
        """
        Comment.objects.create(user=self.user, ad=self.ad, content='Comment 1')
        Comment.objects.create(user=self.user, ad=self.ad, content='Comment 2')

        self.assertEqual(self.ad.comments.count(), 2)

    def test_get_last_month_ads(self) -> None:
        """
        Test that Ad.get_ads_last_month() returns recent ads,
        and excludes ads older than 30 days.
        """
        recent_ads = Ad.get_ads_last_month()
        self.assertIn(self.ad, recent_ads)
        self.assertNotIn(self.old_ad, recent_ads)
