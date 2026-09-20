from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .forms import NoteForm
from .models import Note


def _visible_notes(user=None):
    """Every note in the app - once you are logged in, you can read them all."""
    return (Note.objects
            .all()
            .select_related('owner')
            .prefetch_related('shared_with'))


def _dashboard_stats(user):
    """Numbers on the three cards - all computed live from the database."""
    # Every note is readable by every logged-in user, so "total" means all of them.
    total_notes = Note.objects.count()

    # Notes posted by somebody else that this user can read.
    shared_notes = Note.objects.exclude(owner=user).count()

    # Everyone other than me who has posted at least one note.
    collaborators = (Note.objects
                     .exclude(owner=user)
                     .values('owner')
                     .distinct()
                     .count())

    return {
        'total_notes': total_notes,
        'shared_notes_count': shared_notes,
        'collaborators_count': collaborators,
        'my_notes_count': Note.objects.filter(owner=user).count(),
    }


@login_required
def home(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            note = form.save()
            messages.success(request, f'"{note.subject}" was saved.')
            return redirect('home')
        messages.error(request, 'Your note could not be saved - see the errors below.')
    else:
        form = NoteForm(user=request.user)

    notes = _visible_notes()
    query = request.GET.get('q', '').strip()
    mine_only = request.GET.get('mine') == '1'

    if mine_only:
        notes = notes.filter(owner=request.user)

    if query:
        notes = notes.filter(
            Q(subject__icontains=query)
            | Q(content__icontains=query)
            | Q(tag__icontains=query)
            | Q(owner__username__icontains=query)
            | Q(shared_with__username__icontains=query)
        ).distinct()

    context = {
        'form': form,
        'note': notes,
        'query': query,
        'mine_only': mine_only,
    }
    context.update(_dashboard_stats(request.user))
    return render(request, 'home.html', context)


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user:
        raise PermissionDenied('You can only delete your own notes.')
    if request.method == 'POST':
        subject = note.subject
        if note.file:
            note.file.delete(save=False)
        note.delete()
        messages.success(request, f'"{subject}" was deleted.')
    return redirect('home')


class NoteListView(LoginRequiredMixin, DetailView):
    """Kept for backwards compatibility; the dashboard is served by home()."""
    model = Note


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return _visible_notes()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_dashboard_stats(self.request.user))
        return context
