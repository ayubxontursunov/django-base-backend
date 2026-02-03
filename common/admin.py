from django.contrib import admin
from .models import Region, District, DocumentType

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'created')
    search_fields = ('name', 'code')
    readonly_fields = ('created', 'updated')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'code', 'created')
    list_filter = ('region',)
    search_fields = ('name', 'code', 'region__name')
    readonly_fields = ('created', 'updated')

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created')
    search_fields = ('name',)
    readonly_fields = ('created', 'updated')
