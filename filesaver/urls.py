from django.urls import path
from .views import (
    TaskListCreateView, TaskDetailView, DashboardStatsView,
    RegionListView, DistrictListView, DocumentTypeListView
)

app_name = 'filesaver'

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Common data endpoints
    path('regions/', RegionListView.as_view(), name='region-list'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('document-types/', DocumentTypeListView.as_view(), name='document-type-list'),
]
