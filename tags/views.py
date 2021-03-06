from django.contrib import messages
from django.contrib.messages import add_message
from django.shortcuts import get_object_or_404, redirect, render

from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, remove_perm, get_objects_for_user

from notes.models import Note

from tags.models import GuardedTag
from taggit.utils import parse_tags

from .forms import TagForm


def index(request):
    """
    List of used tags. Filtering by tags options included (tbd).
    :param request: HTTP request.
    """

    context = {
        'tags': get_objects_for_user(request.user, 'tags.view_guardedtag').order_by('name'),
    }
    return render(request, 'tags/index.html', context)


@permission_required_or_403('tags.view_guardedtag', (GuardedTag, 'id', 'tag_id'))
def edit(request, tag_id):
    """
    POST: Edit form for selected tag.
    GET: Display tag form populated with tag's data.
    If changing tag's name, tries to make new tag, gives view perm, and reassigns all notes of that user to it.
    :param tag_id: Selected tag's ID.
    :param request: HTTP request.

    """

    old_tag = get_object_or_404(GuardedTag, pk=tag_id)
    new_tag = GuardedTag()
    tag_list = []

    # POST method - edit existing tag
    if request.method == 'POST':
        form = TagForm(request.POST, instance=new_tag)
        # if form is valid, parse string into tag names
        if form.is_valid():
            tag_words = parse_tags(form.instance.name)
            # in case of more than one name - make a list of tags, otherwise search for one tag or create one
            if len(tag_words) > 1:
                for word in tag_words:
                    tag = GuardedTag.objects.filter(name=word).first()
                    if not tag:
                        tag = GuardedTag(name=word, slug=word)
                        tag.save()
                    tag_list.append(tag)
            else:
                new_tag = GuardedTag.objects.filter(name=tag_words[0]).first()
                if new_tag is None:
                    form.save()

        elif 'Tag with this Name already exists.' in form.errors['name']:
            new_tag = GuardedTag.objects.filter(name=form.instance.name).first()
            # if there is no change provided - just redirect to index
            if new_tag:
                if old_tag.name == new_tag.name:
                    add_message(request, messages.INFO, 'There was no change provided to edited tag.')
                    return redirect('tags:index')
        else:
            new_tag = None

        # deletes permission for the old tag and gives to the new one
        if new_tag is not None or len(tag_list) >= 1:
            if not tag_list:
                tag_list.append(new_tag)
            remove_perm('view_guardedtag', request.user, old_tag)
            # check for notes with the old tag and replace it with the new one
            notes = Note.objects.filter(creator=request.user, tags__name__in=[old_tag.name]).distinct()
            # for safety reason - exclude notes without change perm (even though creator should always has it)
            notes = get_objects_for_user(request.user, 'notes.change_note', klass=notes)
            if notes:
                for note in notes:
                    note.tags.remove(old_tag)
                    for tag in tag_list:
                        assign_perm('view_guardedtag', request.user, tag)
                        note.tags.add(tag)
                add_message(request, messages.INFO, 'Tag changed and replaced in note(s).')
                return redirect('tags:index')

            add_message(request, messages.INFO, 'Tag changed.')
        return redirect('tags:index')

    # GET method - display and populate form with note data
    context = {
        'tags': get_objects_for_user(request.user, 'tags.view_guardedtag').order_by('name'),
        'form': TagForm(initial={
            'name': old_tag.name,
        }),
        'edit_tag_id': tag_id,
    }
    return render(request, 'tags/index.html', context)


@permission_required_or_403('tags.view_guardedtag', (GuardedTag, 'id', 'tag_id'))
def delete(request, tag_id):
    """
    Delete selected tag - gives away view permission, deletes from user's notes,
    and erases tag from DB if no one is using it.
    :param tag_id: Selected tag's ID.
    :param request: HTTP request.
    """

    tag = get_object_or_404(GuardedTag, pk=tag_id)
    notes = Note.objects.filter(creator=request.user, tags__name__in=[tag.name]).distinct()
    for note in notes:
        note.tags.remove(tag)
    remove_perm('view_guardedtag', request.user, tag)
    if notes:
        add_message(request, messages.INFO, 'Tag removed from note(s).')

    # if no one is using this tag - clear db from it
    if not Note.objects.filter(tags__name__in=[tag.name]).all():
        GuardedTag.objects.get(pk=tag_id).delete()

    return redirect('tags:index')
