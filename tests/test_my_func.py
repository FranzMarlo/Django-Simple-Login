import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

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


@pytest.mark.django_db
def test_user_str_method():
    """Test the __str__ method of the CustomUser model."""
    user = User.objects.create_user(username="testuser", password="testpassword")
    assert str(user) == "testuser"


@pytest.mark.django_db
def test_login_view_success():
    """Test that a user can successfully log in."""
    User.objects.create_user(username="testuser", password="testpassword")
    client = Client()
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302  # Redirect to 'home'


@pytest.mark.django_db
def test_login_view_invalid_credentials():
    """Test login with invalid credentials."""
    client = Client()
    response = client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpassword'})
    assert response.status_code == 200  # Stay on the login page
    assert "Invalid username or password." in response.content.decode()


@pytest.mark.django_db
def test_home_view_authenticated_user():
    """Test the home view for an authenticated user."""
    user = User.objects.create_user(username="testuser", password="testpassword")
    client = Client()
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert "Welcome" in response.content.decode()  # Assuming the home page contains 'Welcome'

@pytest.mark.django_db
def test_home_view_unauthenticated_user():
    """Test that an unauthenticated user is redirected to the login page."""
    client = Client()
    response = client.get(reverse('home'))
    assert response.status_code == 302  # Redirect to login
    assert response.url == f"{reverse('login')}?next={reverse('home')}"


@pytest.mark.django_db
def test_logout_view():
    """Test that a logged-in user is successfully logged out."""
    user = User.objects.create_user(username="testuser", password="testpassword")
    client = Client()
    client.login(username='testuser', password='testpassword')
    
    response = client.get(reverse('logout'))
    assert response.status_code == 302  # Redirect to login
    
    # Check that the session no longer contains the authenticated user's ID
    assert '_auth_user_id' not in client.session
