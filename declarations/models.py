from django.db import models
from django.db.models import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

year_list = []


class Office(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=True)
    name = models.TextField(verbose_name='полное название')
    sort_order = models.IntegerField(
        default=0, verbose_name='Порядок сортировки'
    )

    def get_status(self):
        result = []
        for year in year_list:
            file_count = DocumentFile.objects.filter(
                document__income_year=year,
                document__office__id=self.id,
                file__isnull=False
            ).count()
            declaration_count = Document.objects.filter(
                office__id=self.id, income_year=year
            ).count()
            if file_count > 0 and file_count == declaration_count:
                result.append('all_files')
            elif file_count > 0 and file_count != declaration_count:
                result.append('some_files')
            elif file_count == 0 and declaration_count > 0:
                result.append('no_files_but_declaration')
            elif file_count == 0 and declaration_count == 0:
                result.append('nothing')
        return result

    def __str__(self):
        return self.name


class Document(models.Model):

    office = ForeignKey(
        'declarations.Office', verbose_name="орган власти",
        on_delete=True, related_name='documents'
    )
    income_year = models.IntegerField(
        verbose_name="год за который указан доход"
    )

    def __str__(self):
        return 'Документ из организации ' + self.office.name


@receiver(post_save, sender=Document)
def call_refres_year_list(sender, **kwargs):
    refres_year_list()


def refres_year_list():
    year_list = Document.objects.all().distinct(). \
        order_by('-income_year').values_list('income_year', flat=True)
    if len(year_list) == 0:
        return []
    return list(range(year_list[0], year_list[len(year_list)-1]-1, -1)) if len(year_list) > 1 else [year_list[0]]


year_list = refres_year_list()


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document, verbose_name="декларация",
        on_delete=True,
        related_name='files'
    )
    file = models.FileField(
        blank=True, max_length=255, null=True,
        upload_to='uploads/%Y/%m/%d/', verbose_name="файл"
    )

    def __str__(self):
        return 'Файл декларации организации ' + self.document.office.name
