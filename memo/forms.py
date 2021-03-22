from django import forms
from .models import Category, Tag, Question, Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['cat', 'tags', 'title', 'content']
