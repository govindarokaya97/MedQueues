from django.urls import path
from . import views


urlpatterns = [

    path(
            "tests/",
            views.TestListView.as_view(),
            name="test_list"
        ),

    path(
            "tests/add/",
            views.TestCreateView.as_view(),
            name="test_add"
        ),
    
    path(
            "<int:id>/",
            views.TestDetailView.as_view(),
            name="test_detail"
        ),
    
    path(
            "<int:id>edit/",
            views.TestUpdateView.as_view(),
            name="test_edit"
        ),
    
    path(
            "<int:id>delete/",
            views.TestDeleteView.as_view(),
            name="test_delete"
        ),

    path(
            "requests/",
            views.create_lab_request,
            name="request_create"
        ),

    path(
            "requests/list/",
            views.LabRequestListView.as_view(),
            name="request_list"
        ),
    
    path(
            "requests/<int:id>/assign/",
            views.assign_technician,
            name="assign_technician",
        ),
    
    path(
            "requests/<int:id>/report/",
            views.create_lab_report,
            name="create_lab_report"
        ),
    
    path(
            "report/<int:id>/",
            views.report_detail, 
            name="report_detail"
            
        ),
    
    path(
            "report/<int:id>/verify/",
            views.verify_report, 
            name="verify_report"
        )

]