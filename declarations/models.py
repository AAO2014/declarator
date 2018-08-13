from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Office(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=True)
    name = models.TextField(verbose_name='полное название')
    sort_order = models.IntegerField(
        default=0, verbose_name='Порядок сортировки'
    )

    def __str__(self):
        return  self.name


class Document(models.Model):
    office = TreeForeignKey(
        'declarations.Office', verbose_name="орган власти", on_delete=True)
    income_year = models.IntegerField(
        verbose_name="год за который указан доход"
    )


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document, verbose_name="декларация",
        on_delete=True
    )
    file = models.FileField(
        blank=True, max_length=255, null=True,
        upload_to='uploads/%Y/%m/%d/', verbose_name="файл"
    )