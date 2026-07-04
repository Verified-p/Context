pip freeze > requirements.txt

python manage.py collectstatic
python manage.py collectstatic --noinput


from accounts.models import User

User.objects.create_user(
    username="Expertize",
    password="@Hublab!1",
    role="SUPER_ADMIN",
    first_name="System",
    last_name="Administrator",
    email="academicperfect@gmail.com",
    is_staff=True,
    is_superuser=True,
    is_active=True,
    is_verified=True,
)