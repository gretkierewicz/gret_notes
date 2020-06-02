from .models import Note

from django.forms import ModelForm, Textarea, TextInput


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']
        widgets = {
            'title': TextInput(attrs={'size': 130}),
            'body': Textarea(attrs={'cols': 130, 'rows': 20}),
        }
