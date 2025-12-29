
from django.contrib import admin

from .models import Thesis, Author, ThesisType, Institute, Language, University, Keyword, SubjectTopic, Supervisor

admin.site.register(University)
admin.site.register(Thesis)
admin.site.register(Author)
admin.site.register(ThesisType)
admin.site.register(Institute)
admin.site.register(Supervisor)    
admin.site.register(SubjectTopic)
admin.site.register(Language)
admin.site.register(Keyword)


class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'thesis_no', 'author', 'year', 'language', 'type')
    list_filter = ('year', 'language', 'type', 'institute')
    search_fields = ('title', 'author__name', 'thesis_no')
    filter_horizontal = ('keywords', 'topics')
    