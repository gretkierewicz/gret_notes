from django.shortcuts import render

from .models import Note


def index(request):
    note_list = Note.objects.order_by('-create_time')

    context = {
        'note_list': note_list,
    }
    return render(request, 'notes/index.html', context)
