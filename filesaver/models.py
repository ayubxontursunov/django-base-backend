from django.db import models
from common.models import BaseModel


class Task(BaseModel):
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    region = models.ForeignKey('common.Region', on_delete=models.CASCADE)
    district = models.ForeignKey('common.District', on_delete=models.CASCADE)
    document_type = models.ForeignKey('common.DocumentType', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Document Date')
    short_summary = models.TextField(verbose_name='Short Summary')
    status = models.CharField(max_length=255, verbose_name='Status', choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ))

    class Meta:
        verbose_name_plural = "Tasks"
        verbose_name = "Task"


class File(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')

    class Meta:
        verbose_name_plural = "Files"
        verbose_name = "File"
