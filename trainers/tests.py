from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TrainerProfile

User = get_user_model()


class TrainerTest(TestCase):

    def test_create_trainer_profile(self):

        user = User.objects.create_user(
            username="trainer1",
            password="testpass123",
            role="TRAINER"
        )

        trainer = TrainerProfile.objects.create(
            user=user,
            full_name="Test Trainer"
        )

        self.assertEqual(trainer.full_name, "Test Trainer")