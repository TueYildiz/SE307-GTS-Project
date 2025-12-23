
from django.contrib import admin

from .models import Thesis, Author, ThesisType, Institute, Language


admin.site.register(Thesis)
admin.site.register(Author)
admin.site.register(ThesisType)
admin.site.register(Institute)
admin.site.register(Language)