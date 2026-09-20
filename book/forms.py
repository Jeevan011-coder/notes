from django import forms
from django.contrib.auth.models import User

from .models import ALLOWED_EXTENSIONS, Note

MAX_UPLOAD_MB = 10


class NoteForm(forms.ModelForm):
    """Create a note from text, a PDF, or a JPG/JPEG - and optionally share it."""

    share_with = forms.CharField(
        required=False,
        label='Share with',
        widget=forms.TextInput(attrs={
            'class': 'share-input',
            'placeholder': 'Usernames or emails, comma separated...',
        }),
        help_text='Comma separated usernames or emails of registered users.',
    )

    class Meta:
        model = Note
        fields = ['subject', 'tag', 'content', 'file']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'note-input-title',
                'placeholder': 'Note title...',
            }),
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write something worth sharing...',
            }),
            'tag': forms.Select(attrs={'class': 'tag-select'}),
            'file': forms.ClearableFileInput(attrs={
                'accept': '.pdf,.jpg,.jpeg,application/pdf,image/jpeg',
            }),
        }

    def __init__(self, *args, **kwargs):
        # The view passes the logged-in user so we can stop self-sharing.
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False
        self.fields['file'].required = False

    def clean_file(self):
        uploaded = self.cleaned_data.get('file')
        if not uploaded:
            return uploaded

        name = uploaded.name.lower()
        if not name.endswith(tuple('.' + ext for ext in ALLOWED_EXTENSIONS)):
            raise forms.ValidationError('Only PDF, JPG and JPEG files are allowed.')

        if uploaded.size > MAX_UPLOAD_MB * 1024 * 1024:
            raise forms.ValidationError(f'File must be smaller than {MAX_UPLOAD_MB} MB.')

        return uploaded

    def clean_share_with(self):
        raw = self.cleaned_data.get('share_with', '')
        handles = [part.strip() for part in raw.replace(';', ',').split(',') if part.strip()]
        if not handles:
            return []

        users, unknown = [], []
        for handle in handles:
            match = User.objects.filter(username__iexact=handle).first() \
                or User.objects.filter(email__iexact=handle).first()
            if match is None:
                unknown.append(handle)
            elif self.user is None or match.pk != self.user.pk:
                users.append(match)

        if unknown:
            raise forms.ValidationError('No registered user found for: ' + ', '.join(unknown))

        return users

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('content') and not cleaned.get('file'):
            raise forms.ValidationError(
                'Add some text or attach a PDF/JPEG file - a note cannot be empty.'
            )
        return cleaned

    def save(self, commit=True):
        note = super().save(commit=False)
        if self.user is not None:
            note.owner = self.user
        if commit:
            note.save()
            note.shared_with.set(self.cleaned_data.get('share_with') or [])
        return note
