from accounts.models import User

User.objects.create_user(
    username="context",
    password="@Hublab!1",
    role="SUPER_ADMIN",
    first_name="Context",
    last_name="Administrator",
    email="academicperfect@gmail.com",
    is_staff=True,
    is_superuser=True,
    is_active=True,
    is_verified=True,
)