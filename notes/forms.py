from .models import Note

from django.forms import ModelForm, Textarea, TextInput


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'tags']
        widgets = {
            'title': TextInput(attrs={'size': 128, 'required': True}),
            'body': Textarea(attrs={'cols': 130, 'rows': 20}),
            'tags': TextInput(attrs={'size': 128}),
        }
