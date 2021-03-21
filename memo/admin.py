from django.contrib import admin
from memo.models import Category, Tag, Question, Note


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('cat__name', 'tags__name', 'answer', 'problem')


class NoteAdmin(admin.ModelAdmin):
    search_fields = ('cat__name', 'tags__name', 'title', 'content')


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Note, NoteAdmin)
