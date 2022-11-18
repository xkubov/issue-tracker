import typing

import pytest

from ..models import Issue


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
    create_issue: typing.Callable[..., Issue], timezone_patcher: typing.Any
) -> None:
    """
    Test opened_at is set to the current time.
    """
    expected = timezone_patcher._now
    issue = create_issue(state=Issue.State.CLOSED)
    assert issue.opened_at == expected


@pytest.mark.django_db
def test_open_closed_issue(
    create_issue: typing.Callable[..., Issue], timezone_patcher: typing.Any
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
    create_issue: typing.Callable[..., Issue], timezone_patcher: typing.Any
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
