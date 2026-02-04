from django.db import models
from common.models import BaseModel


class Task(BaseModel):
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE)
    region = models.ForeignKey('common.Region', on_delete=models.CASCADE)
    district = models.ForeignKey('common.District', on_delete=models.CASCADE)
    document_type = models.ForeignKey('common.DocumentType', on_delete=models.CASCADE)
    # Mandatory Fields
    sender_org_name = models.CharField(max_length=500, verbose_name='Yuboruvchi tashkilot nomi')
    document_title = models.CharField(max_length=500, verbose_name='Hujjat sarlavhasi / Qisqacha mazmuni')
    received_date = models.DateField(verbose_name='Kelib tushgan sana')
    received_channel = models.CharField(
        max_length=255, 
        verbose_name='Kelib tushish kanali',
        choices=(
            ('courier', 'Kuryer'),
            ('mail', 'Pochta'),
            ('email', 'Elektron pochta'),
            ('portal', 'Portal'),
            ('hand_delivery', 'Qo\'lda'),
            ('other', 'Boshqa'),
        ),
        default='courier'
    )
    sensitivity_level = models.CharField(
        max_length=255, 
        verbose_name='Maxfiylik darajasi',
        choices=(
            ('normal', 'Oddiy'),
            ('for_official_use', 'Xizmat doirasida foydalanish uchun'),
            ('confidential', 'Maxfiy'),
        ),
        default='normal'
    )

    # Optional Fields
    incoming_ref_number = models.CharField(max_length=255, verbose_name='Kirish raqami', blank=True, null=True)
    incoming_ref_date = models.DateField(verbose_name='Kirish sanasi', blank=True, null=True)
    sender_person_name = models.CharField(max_length=255, verbose_name='Yuboruvchi shaxs ismi', blank=True, null=True)
    sender_person_position = models.CharField(max_length=255, verbose_name='Yuboruvchi lavozimi', blank=True, null=True)
    document_language = models.CharField(
        max_length=10, 
        verbose_name='Hujjat tili',
        choices=(
            ('uz', 'O\'zbek'),
            ('ru', 'Rus'),
            ('en', 'Ingliz'),
        ),
        blank=True,
        null=True
    )

    status = models.CharField(max_length=255, verbose_name='Status', choices=(
        ('pending', 'Jarayonda'),
        ('completed', 'Bajarildi'),
    ), default='pending')

    class Meta:
        verbose_name_plural = "Tasks"
        verbose_name = "Task"

    def __str__(self):
        return f"{self.id} - {self.creator.full_name} - {self.document_type.name}"


class File(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')

    class Meta:
        verbose_name_plural = "Files"
        verbose_name = "File"
