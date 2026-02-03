from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Regions"
        verbose_name = "Region"

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Districts"
        verbose_name = "District"

    def __str__(self):
        return self.name


class DocumentType(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Document Types"
        verbose_name = "Document Type"

    def __str__(self):
        return self.name
