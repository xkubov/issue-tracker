from rest_framework import serializers

from .models import Issue


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer of Issue model into the list/summary JSON representation.
    """

    category = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()
    submitter = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "submitter",
            "assignee",
            "state",
            "category",
            "opened_at",
        ]

    def get_category(self, obj: Issue) -> str:
        """A custom serializer for category field returning its string repr."""
        return str(obj.category)

    def get_assignee(self, obj: Issue) -> str:
        """A custom serializer for assignee field returning its streing repr."""
        return str(obj.assignee)

    def get_submitter(self, obj: Issue) -> str:
        """A custom serializer for submitter field returning its streing repr."""
        return str(obj.assignee)


class IssueSerializer(IssueListSerializer):
    """
    Serializer of Issue model into the detailed JSON representation.
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "submitter",
            "assignee",
            "state",
            "category",
            "opened_at",
        ]
