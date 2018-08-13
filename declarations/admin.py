from django.contrib import admin

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mptt.admin import MPTTModelAdmin

from declarations.models import Office, Document, DocumentFile

admin.site.register(Office, MPTTModelAdmin)
admin.site.register(Document, ModelAdmin)
admin.site.register(DocumentFile, ModelAdmin)