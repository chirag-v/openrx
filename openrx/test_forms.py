# openrx/tests/test_forms.py
import pytest
from django.contrib.auth.models import User
from openrx.forms import LoginForm

@pytest.mark.django_db
def test_login_form_valid_data():
    # Create the user before validating the form
    User.objects.create_user(username='testuser', password='password123')

    form_data = {'username': 'testuser', 'password': 'password123'}
    form = LoginForm(data=form_data)
    assert form.is_valid(), f"Form errors: {form.errors}"

@pytest.mark.django_db
def test_login_form_invalid_data():
    form_data = {'username': '', 'password': ''}
    form = LoginForm(data=form_data)
    assert not form.is_valid()
    assert 'username' in form.errors
    assert 'password' in form.errors