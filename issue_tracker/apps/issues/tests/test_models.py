import typing
from datetime import datetime, timedelta

import pytest
from django.contrib.auth import get_user_model

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
    yield TimezonePatcher(datetime(year=2022, month=11, day=18), mocker)


@pytest.mark.django_db
@pytest.fixture()
def create_issue() -> typing.Callable[..., Issue]:
    def do_create(state: Issue.State, title: str = "Title") -> Issue:
        cls = get_user_model()
        user = cls(
            username="tester",
            password="secret",
            email="tester@testing",
            is_superuser=False,
            is_staff=True,
        )
        user.save()

        category = Category(name="testing_category")
        category.save()

        issue = Issue(
            title=title,
            description="Test description",
            submitter=user,
            assignee=user,
            state=state,
            category=category,
        )

        issue.save()

        return issue

    return do_create


@pytest.mark.django_db
def test_issues_are_identified_by_title(create_issue: typing.Callable[..., Issue]) -> None:
    """
    Test __str__ method of Issue works as expected.
    """
    issue = create_issue(state=Issue.State.CLOSED, title="My Awesome Title")
    assert "My Awesome Title" == str(issue)


@pytest.mark.django_db
def test_categories_are_identified_by_name(create_issue: typing.Callable[..., Issue]) -> None:
    """
    Test __str__ method of Category works as expected.
    """
    issue = create_issue(state=Issue.State.CLOSED)
    assert issue.category.name == str(issue.category)


@pytest.mark.django_db
def test_created_closed_issue_is_solved_instantly(
    create_issue: typing.Callable[..., Issue]
) -> None:
    """
    Test opening closed issue sets resolution duration to 0.
    """
    issue = create_issue(state=Issue.State.CLOSED)
    assert issue.resolution_duration == 0


@pytest.mark.django_db
def test_opened_at_is_set(
    create_issue: typing.Callable[..., Issue], timezone_patcher: TimezonePatcher
) -> None:
    """
    Test opened_at is set to the current time.
    """
    expected = timezone_patcher._now
    issue = create_issue(state=Issue.State.CLOSED)
    assert issue.opened_at == expected


@pytest.mark.django_db
def test_open_closed_issue(
    create_issue: typing.Callable[..., Issue], timezone_patcher: TimezonePatcher
) -> None:
    """
    Test opening closed issue changes `opened_at` field and doesn't change resolution_duration.
    """
    issue = create_issue(state=Issue.State.CLOSED)
    opened_at_before = issue.opened_at

    # Open the issue
    issue.state = Issue.State.OPEN
    issue.save()

    assert opened_at_before != issue.opened_at
    assert issue.resolution_duration == 0


@pytest.mark.django_db
def test_close_opened_issue(
    create_issue: typing.Callable[..., Issue], timezone_patcher: TimezonePatcher
) -> None:
    """
    Test opening closed issue doesn't change `opened_at` field and changes resolution_duration.
    """
    issue = create_issue(state=Issue.State.OPEN)
    opened_at_before = issue.opened_at

    # Close the issue
    issue.state = Issue.State.CLOSED
    issue.save()

    assert opened_at_before == issue.opened_at
    assert issue.resolution_duration == 1
