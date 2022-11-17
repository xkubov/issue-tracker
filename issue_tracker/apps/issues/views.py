from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Issue
from .serializers import IssueSerializer, IssueListSerializer


@api_view(["GET"])
def issues_list(request: HttpRequest) -> HttpResponse:
    """
    List all issues.
    """
    issues = Issue.objects.all()
    serializer = IssueListSerializer(issues, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def issue_detail(request: HttpRequest, iid: int) -> HttpResponse:
    """
    List all issues.
    """
    try:
        issue = Issue.objects.get(id=iid)

    except Issue.DoesNotExist:
        return JsonResponse(data={"error": "Not found."}, status=404)

    serializer = IssueSerializer(issue)
    return Response(serializer.data)
