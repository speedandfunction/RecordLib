"""
Tests for the webapp's user profile views and authentication.
"""

import pytest
from django.contrib.auth.models import User
from cleanslate.models import UserProfile


def test_anonymous_cannot_get_userprofileview(dclient):
    """ Anonymous user can't access the user profile view."""
    resp = dclient.get("/api/record/profile/", follow=True)
    assert resp.status_code == 403


def test_loggedin_get_userprofileview(admin_client):
    """A logged in user can access the user profile view."""
    resp = admin_client.get("/api/record/profile/", follow=True)
    assert resp.status_code == 200
    userdata = resp.data
    assert "user" in userdata.keys()
    assert "profile" in userdata.keys()


@pytest.mark.django_db
def test_user_profile_created_on_postsave():
    usr = User.objects.create_user(username="Test", password="test")
    usr.save()
    try:
        usr.userprofile
    except:
        pytest.fail("usr doesn't seem to have a profile attached to it")

