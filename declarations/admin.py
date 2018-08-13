from django.contrib import admin

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from declarations.models import Office


admin.site.register(Office, MPTTModelAdmin)