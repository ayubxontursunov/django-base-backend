from rest_framework import serializers
from .models import Task, File
from common.models import Region, District, DocumentType

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'created']

class TaskSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True, source='file_set')
    creator_name = serializers.CharField(source='creator.full_name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'creator', 'creator_name', 'region', 'region_name', 
            'district', 'district_name', 'document_type', 'document_type_name', 
            'sender_org_name', 'document_title', 'received_date', 'received_channel',
            'sensitivity_level', 'incoming_ref_number', 'incoming_ref_date',
            'sender_person_name', 'sender_person_position', 'document_language',
            'status', 'files', 'created', 'uploaded_images'
        ]
        read_only_fields = ['creator', 'created']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        task = Task.objects.create(**validated_data)
        
        if uploaded_images:
            for image in uploaded_images:
                File.objects.create(task=task, file=image)
        
        return task

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        
        # Update standard fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Append new files if any
        if uploaded_images:
            for image in uploaded_images:
                File.objects.create(task=instance, file=image)
        
        return instance

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
