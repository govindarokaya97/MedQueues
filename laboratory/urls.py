from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.TestListView.as_view(),
        name="test_list"
    ),

    path(
        "add/",
        views.TestCreateView.as_view(),
        name="test_add"
    ),

    path(
        "<int:id>/",
        views.TestDetailView.as_view(),
        name="test_detail"
    ),

    path(
        "<int:id>/edit/",
        views.TestUpdateView.as_view(),
        name="test_edit"
    ),

    path(
        "<int:id>/delete/",
        views.TestDeleteView.as_view(),
        name="test_delete"
    ),
]