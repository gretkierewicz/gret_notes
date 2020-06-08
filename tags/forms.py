from django.forms import ModelForm, TextInput

from taggit.models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'size': 24})
        }
