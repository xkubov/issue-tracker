"""
Models for the issues app.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    A model for category of issues

    Even thought the category is a simple model we want it separated from the Issue.
    In the future, we may want to add the option to manage categories dynamically
    (from the admin site).
    """

    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Issue(models.Model):
    """Representation of issue."""

    class State(models.TextChoices):
        """States of an issue"""

        OPEN = "OPN"
        CLOSED = "CLS"

    title = models.CharField(
        max_length=80,
        help_text="A brief description of the issue.",
    )
    description = models.TextField(
        help_text="A detailed description of the issue.",
    )
    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(class)s_submitted",
        help_text="The reporter of the issue.",
    )
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="%(class)s_assigned",
        help_text="Assign a user to resolve this issue.",
    )
    state = models.CharField(
        max_length=3,
        choices=State.choices,
        default=State.OPEN,
        help_text="The current state of the issue.",
    )
    previous_state = models.CharField(
        max_length=3,
        choices=State.choices,
        default=State.OPEN,
        editable=False,
        help_text="Previous state of the issue.",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text="The category best suited for the issue.",
    )
    opened_at = models.DateTimeField(
        auto_now_add=True,
        help_text="A datetime of opening issue. Updated when the issue is moved to open state.",
    )
    resolution_duration = models.IntegerField(
        default=0,
        editable=False,
        help_text="The time in seconds the issue was in open state.",
    )

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        # If the state is being udated we want to ensure that:
        # * update Open -> Closed will update the `resolution_duration` time.
        # * update Close -> Open will mark the opening time of the issue.

        if self.previous_state != self.state:
            if self.state == Issue.State.CLOSED:
                # We can create issue in closed state. In that case we don't want
                # to do any action.
                if self.opened_at is not None:
                    resolution_delta = timezone.now() - self.opened_at
                    self.resolution_duration += int(resolution_delta.total_seconds())

            else:
                self.opened_at = timezone.now()

        self.previous_state = self.state

        super().save(*args, **kwargs)
