from django.contrib import admin
from .models import Task, File

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'region', 'district', 'document_type', 'sender_org_name', 'received_date', 'status', 'created')
    list_filter = ('status', 'region', 'district', 'document_type', 'received_date', 'received_channel', 'sensitivity_level')
    search_fields = ('document_title', 'sender_org_name', 'creator__username', 'creator__email', 'creator__full_name')
    date_hierarchy = 'received_date'
    readonly_fields = ('created', 'updated')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'file', 'created')
    list_filter = ('created',)
    search_fields = ('task__short_summary',)
    readonly_fields = ('created', 'updated')
