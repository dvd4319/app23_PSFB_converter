from django.contrib import admin
from .models import FullBridgePhaseShiftConverter
from import_export.admin import ImportExportModelAdmin 



class FullBridgePhaseShiftConverterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ... 



admin.site.register(FullBridgePhaseShiftConverter, FullBridgePhaseShiftConverterAdmin )
