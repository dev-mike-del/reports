from django.contrib import admin

from report_types.models import BasicReport, BasicReportVersion


class BasicReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)

class BasicReportVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)


admin.site.register(BasicReport, BasicReportAdmin)
admin.site.register(BasicReportVersion, BasicReportVersionAdmin)
