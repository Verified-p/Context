from .models import TrainerProfile


def create_trainer_profile(user, full_name):
    """
    Auto create trainer profile
    """
    return TrainerProfile.objects.create(
        user=user,
        full_name=full_name
    )