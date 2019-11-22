from django.contrib import admin

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_created', 'date_modified',
    	'created_by', 'modified_by')
    list_display_links = ('id', 'title', 'date_created', 'date_modified',
    	'created_by', 'modified_by')
    order = ('id',)
    list_filter = ['id', 'title', 'date_created', 'date_modified',
    	'created_by', 'modified_by']
    search_fields = ['title']
    list_per_page = 20 

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user.username
        else:
        	obj.modified_by = request.user.username
        obj.save()


admin.site.register(Tag, TagAdmin)