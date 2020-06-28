from .models import Note

from django.forms import ModelForm, TextInput
from django_summernote.widgets import SummernoteWidget


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'tags']
        widgets = {
            'title': TextInput(attrs={'size': 128}),
            'body':  SummernoteWidget(attrs={
                'summernote': {
                    'toolbar': [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript', 'hr']],
                        ['fontname', ['fontname']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['insert', ['link', 'picture']],
                    ],
                }
            }),
            'tags': TextInput(attrs={'size': 128}),
        }
