from django.contrib import messages
from django.contrib.messages import add_message
from django.shortcuts import get_object_or_404, redirect, render

from guardian.decorators import permission_required_or_403
from guardian.shortcuts import remove_perm, get_objects_for_user

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
    # TBD
    return redirect('tags:index')


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
