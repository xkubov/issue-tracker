import typing

from django.contrib import admin
from django.db.models import Avg, Max, Min
from django.http.request import HttpRequest
from django.template.response import TemplateResponse

from issue_tracker.common.utils import duration

from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):  # type: ignore
    """
    A custom admin page to personalize list of issues for purpose of this app.
    """

    list_display = (
        "__str__",
        "state",
        "assignee",
        "opened_at",
    )

    def has_module_permission(self, request: HttpRequest) -> bool:
        """Assure staff can view issues module in the admin site."""
        user = request.user
        return getattr(user, "is_staff", False)

    def has_view_permission(self, request: HttpRequest, obj: typing.Any = None) -> bool:
        """Assure staff can view issues in the admin site."""
        user = request.user
        return getattr(user, "is_staff", False)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Assure staff can add issues in the admin site."""
        user = request.user
        return getattr(user, "is_staff", False)

    def has_change_permission(self, request: HttpRequest, obj: typing.Any = None) -> bool:
        """Assure staff CANNOT change issues in the admin site."""
        user = request.user
        return getattr(user, "is_superuser", False)

    def has_delete_permission(self, request: HttpRequest, obj: typing.Any = None) -> bool:
        """Assure staff CANNOT delete issues in the admin site."""
        user = request.user
        return getattr(user, "is_superuser", False)

    def changelist_view(
        self, request: HttpRequest, extra_context: dict[str, typing.Any] | None = None
    ) -> TemplateResponse:
        """
        Custom implementation of list_view. Additional features include:

        * Added statistics to be included by template.
        * Changed title of issues admin page.
        """

        extra_context = extra_context or {}

        stats: dict[str, typing.Any] = {
            "open_issues": Issue.objects.filter(state=Issue.State.OPEN).count(),
            "resolved_issues": Issue.objects.filter(state=Issue.State.CLOSED).count(),
        }

        query = (
            Issue.objects.filter(state=Issue.State.CLOSED)
            .aggregate(
                fastest_resolution=Min("resolution_duration"),
                longest_resolution=Max("resolution_duration"),
                average_resolution=Avg("resolution_duration"),
            )
            .items()
        )

        for aggregation, total_seconds in query:
            stats[aggregation] = duration(total_seconds)

        extra_context.update(
            title="Tracked Issues",
            stats=stats,
        )
        return super().changelist_view(request, extra_context)
