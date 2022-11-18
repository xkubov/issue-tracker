import typing
from datetime import datetime, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Category, Issue


class TimezonePatcher:
    """
    A helper class used for testing time.

    Patches django.utils.timezone.now function. Simulates the passage of time by
    increasing the number of seconds everytime the `timezone.now()` is called.
    """

    def __init__(self, now: datetime, mocker: typing.Any) -> None:
        self._now = now
        mocker.patch("django.utils.timezone.now", wraps=self._patched_now)

    def _patched_now(self) -> datetime:
        """
        Helper method used for patching timezone.now(). Increases _now by one second
        and returns old value of _now.
        """
        to_return = self._now
        self._now += timedelta(seconds=1)
        return to_return

    @property
    def now(self):
        """
        Access method for self._now.
        """
        return self._now


@pytest.fixture()
def timezone_patcher(mocker: typing.Any) -> typing.Generator[TimezonePatcher, None, None]:
    """
    Fixture for accessing timezone patcher.
    """
    yield TimezonePatcher(timezone.datetime(year=2022, month=11, day=18), mocker)


@pytest.mark.django_db
@pytest.fixture()
def create_issue() -> typing.Callable[..., Issue]:
    """
    A factory for initializing issue. Creates users, category and
    issue itself based on it's title.
    """

    def do_create(state: Issue.State, title: str = "Title") -> Issue:
        cls = get_user_model()
        assignee = cls(
            username=f"{title}-assignee",
            password="secret",
            email=f"{title}-assignee@testing",
            is_superuser=False,
            is_staff=True,
        )
        assignee.save()
        submitter = cls(
            username=f"{title}-submitter",
            password="secret",
            email=f"{title}-submitter@testing",
            is_superuser=False,
            is_staff=True,
        )
        submitter.save()

        category = Category(name=f"{title}-category")
        category.save()

        issue = Issue(
            title=title,
            description="Test description",
            submitter=submitter,
            assignee=assignee,
            state=state,
            category=category,
        )

        issue.save()

        return issue

    return do_create
