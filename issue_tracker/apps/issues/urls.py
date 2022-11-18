from django.urls import path

from . import views

urlpatterns = [
    path("issues/", views.issues_list, name="issues"),
    path("issues/<int:iid>/", views.issue_detail, name="issue"),
]
