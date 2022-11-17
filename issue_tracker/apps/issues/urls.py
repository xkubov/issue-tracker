from django.urls import path
from . import views

urlpatterns = [
    path("issues/", views.issues_list),
    path("issues/<int:iid>/", views.issue_detail),
]
