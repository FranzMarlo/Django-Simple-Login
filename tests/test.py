import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    """Test creating a regular user."""
    user = User.objects.create_user(username="testuser", password="testpassword")
    assert user.username == "testuser"
    assert user.check_password("testpassword")  # Verify password is set correctly
    assert not user.is_superuser  # Regular users should not be superusers

@pytest.mark.django_db
def test_create_superuser():
    """Test creating a superuser."""
    superuser = User.objects.create_superuser(username="adminuser", password="adminpassword")
    assert superuser.username == "adminuser"
    assert superuser.check_password("adminpassword")
    assert superuser.is_admin  # Superuser should have is_admin set to True

@pytest.mark.django_db
def test_create_user_without_username():
    """Test that creating a user without a username raises a ValueError."""
    with pytest.raises(ValueError, match="The Username field is required"):
        User.objects.create_user(username=None, password="testpassword")
