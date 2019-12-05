from django.contrib import admin

from status.models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)


admin.site.register(Status, StatusAdmin)
