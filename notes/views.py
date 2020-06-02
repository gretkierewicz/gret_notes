import datetime

from django.contrib import messages
from django.contrib.messages import add_message
from django.shortcuts import get_object_or_404, render, redirect

from .forms import NoteForm
from .models import Note


def index(request):

    note_list = Note.objects.order_by('-create_time')
    context = {
        'note_list': note_list,
    }
    return render(request, 'notes/index.html', context)


def new(request):

    # POST method - create new note
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            form.save()
            add_message(request, messages.INFO, 'Note created succesfuly.')
            return redirect('notes:index')
        else:
            add_message(request, messages.INFO, 'Something gone wrong!.')
            return redirect('notes:index')
    # GET method - display clean form
    else:
        return render(request, 'notes/new.html', {'form': NoteForm()})


def edit(request, note_id):

    note = get_object_or_404(Note, pk=note_id)

    # POST method - edit existing note
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            add_message(request, messages.INFO, 'Note edited succesfuly.')
            return redirect('notes:index')
        else:
            add_message(request, messages.INFO, 'Something gone wrong!')
            return redirect('notes:index')
    # GET method - populate form with note data
    else:
        form = NoteForm(initial={
            'title': note.title,
            'body': note.body,
        })
        context = {
            'note': note,
            'form': form,
        }
        return render(request, 'notes/edit.html', context)


def delete(request, note_id):

    note = get_object_or_404(Note, pk=note_id)
    if note:
        note.delete()
        add_message(request, messages.INFO, 'Note deleted succesfuly.')
    return redirect('notes:index')
