import datetime

from django.contrib import messages
from django.contrib.messages import add_message
from django.shortcuts import get_object_or_404, render, redirect

from guardian import utils
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, get_objects_for_user

from .forms import NoteForm
from .models import Note


def index(request):

    utils.clean_orphan_obj_perms()
    notes = get_objects_for_user(request.user, 'notes.view_note').order_by('-updated_at')

    context = {
        'notes': notes,
    }
    return render(request, 'notes/index.html', context)


def new(request):

    # POST method - create new note
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.creator = request.user
            note.save()
            # save m2m for taggit's tags
            form.save_m2m()
            # assign all rights to the creator
            assign_perm('view_note', request.user, note)
            assign_perm('change_note', request.user, note)
            assign_perm('delete_note', request.user, note)
            add_message(request, messages.INFO, 'Note created succesfuly.')
            return redirect('notes:index')
        else:
            add_message(request, messages.INFO, 'Something gone wrong!.')
            return redirect('notes:index')
    # GET method - display clean form
    else:
        return render(request, 'notes/new.html', {'form': NoteForm()})


@permission_required_or_403('notes.change_note', (Note, 'id', 'note_id'))
def edit(request, note_id):

    note = get_object_or_404(Note, pk=note_id)

    # POST method - edit existing note
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.updated_at = datetime.datetime.now()
            note.save()
            # save m2m for taggit's tags
            form.save_m2m()
            add_message(request, messages.INFO, 'Note edited succesfuly.')
            return redirect('notes:index')
        else:
            add_message(request, messages.INFO, 'Something gone wrong!')
            return redirect('notes:index')
    # GET method - populate form with note data
    else:
        context = {
            'note': note,
            # pre-populate note's form when editing
            'form': NoteForm(initial={
                'title': note.title,
                'body': note.body,
                'tags': ', '.join(list(note.tags.names())),
            }),
        }
        return render(request, 'notes/edit.html', context)


@permission_required_or_403('notes.delete_note', (Note, 'id', 'note_id'))
def delete(request, note_id):

    note = get_object_or_404(Note, pk=note_id)
    if note:
        # not sure if clear is necessary, left just in case
        note.tags.clear()
        note.delete()
        add_message(request, messages.INFO, 'Note deleted succesfuly.')
    return redirect('notes:index')
