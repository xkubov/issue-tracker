from django.contrib import admin
from django.db.models import Avg, Max, Min

from issue_tracker.common.utils import duration

from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """
    A custom admin page to personalize list of issues for purpose of this app.
    """

    list_display = (
        "__str__",
        "state",
        "assignee",
        "opened_at",
    )

    def changelist_view(self, *args, extra_context=None, **kwargs):
        extra_context = extra_context or {}

        stats = {
            k: duration(v)
            for k, v in Issue.objects.filter(state=Issue.State.CLOSED)
            .aggregate(
                fastest_resolution=Min("resolution_duration"),
                longest_resolution=Max("resolution_duration"),
                average_resolution=Avg("resolution_duration"),
            )
            .items()
        }

        extra_context.update(
            title="Tracked Issues",
            stats={
                "open_issues": Issue.objects.filter(state=Issue.State.OPEN).count(),
                "resolved_issues": Issue.objects.filter(state=Issue.State.CLOSED).count(),
                **stats,
            },
        )
        return super().changelist_view(*args, extra_context=extra_context, **kwargs)
