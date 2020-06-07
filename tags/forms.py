from django.forms import ModelForm, TextInput

from taggit.models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Edit'
        }
        widgets = {
            'name': TextInput(attrs={'size': 32, 'required': True})
        }
