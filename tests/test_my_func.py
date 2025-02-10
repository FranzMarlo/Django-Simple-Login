import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_superuser():
    """Test creating a superuser."""
    superuser = User.objects.create_superuser(username="adminuser", password="adminpassword")
    assert superuser.username == "adminuser"
    assert superuser.check_password("adminpassword")
    assert superuser.is_superuser  # Correct field

@pytest.mark.django_db
def test_create_user_without_username():
    """Test that creating a user without a username raises a ValueError."""
    with pytest.raises(ValueError, match="The given username must be set"):
        User.objects.create_user(username=None, password="testpassword")

