from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from .models import Task, File
from .serializers import (
    TaskSerializer, RegionSerializer, DistrictSerializer, DocumentTypeSerializer
)
from common.models import Region, District, DocumentType
from django.utils import timezone

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.select_related(
            'creator', 'region', 'district', 'document_type'
        ).prefetch_related('file_set').all().order_by('-created')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        
        today = timezone.now().date()
        today_docs = Task.objects.filter(created__date=today).count()
        
        # Files count - simplified for now
        total_files = File.objects.count()

        return Response({
            'total_files': total_files,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'today_docs': today_docs
        })

class RegionListView(generics.ListAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()

class DistrictListView(generics.ListAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()

class DocumentTypeListView(generics.ListAPIView):
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()
