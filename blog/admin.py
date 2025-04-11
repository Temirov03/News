from .models import *
from django.contrib import admin
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'category')
    search_fields = ('title', 'category')

admin.site.register(Category)
admin.site.register(Author) 
admin.site.register(Information)
admin.site.register(Presentation)
admin.site.register(HelpGuide)
admin.site.register(OfficialDocument)