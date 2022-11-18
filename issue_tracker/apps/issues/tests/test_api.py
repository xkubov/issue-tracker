import typing

import pytest
from django.urls import reverse
from pytest_drf import APIViewTest, Returns200, UsesGetMethod

from ..models import Issue


@pytest.fixture()
def issues(create_issue: typing.Callable[..., Issue]) -> list[Issue]:
    """
    Creates example issues for later testing.
    """

    examples = [
        create_issue(Issue.State.OPEN, title="Issue1"),
        create_issue(Issue.State.OPEN, title="Issue2"),
        create_issue(Issue.State.OPEN, title="Issue3"),
        create_issue(Issue.State.OPEN, title="Issue4"),
    ]

    return examples


@pytest.mark.django_db
class TestListIssues(APIViewTest, UsesGetMethod, Returns200):  # type: ignore
    @pytest.fixture
    def url(self) -> str:
        return reverse("issues")

    def test_returns_empty_list_of_issues(
        self, json: dict[str, typing.Any] | list[typing.Any]
    ) -> None:
        """
        Tests an empty list of issues is returned.
        """
        assert json == []

    def test_returns_list_of_created_issues(
        self,
        timezone_patcher: typing.Any,
        issues: list[Issue],
        json: dict[str, typing.Any] | list[typing.Any],
    ) -> None:

        """
        Tests expected list of issues is returned.
        """

        expected = [
            {
                "assignee": str(issue.assignee),
                "category": str(issue.category),
                "id": i + 1,
                "opened_at": f"2022-11-18T00:00:{i:02d}+01:00",
                "state": "OPN",
                "submitter": str(issue.submitter),
                "title": issue.title,
            }
            for i, issue in enumerate(issues, 0)
        ]

        assert json == expected


@pytest.mark.django_db
class TestListIssueDetail(APIViewTest, UsesGetMethod):  # type: ignore
    @pytest.fixture
    def url(self) -> str:
        return reverse("issue", args=[1])

    def test_not_found(
        self,
        json: dict[str, typing.Any] | list[typing.Any],
    ) -> None:
        """
        Tests expected error is returned.
        """

        assert json == {"error": "Not found."}

    def test_found(
        self,
        timezone_patcher: typing.Any,
        issues: list[Issue],
        json: dict[str, typing.Any] | list[typing.Any],
    ) -> None:
        """
        Tests an expected issue is returned.
        """

        issue = issues[0]
        expected = {
            "assignee": str(issue.assignee),
            "description": issue.description,
            "category": str(issue.category),
            "id": 1,
            "opened_at": "2022-11-18T00:00:00+01:00",
            "state": "OPN",
            "submitter": str(issue.submitter),
            "title": issue.title,
        }

        assert json == expected
