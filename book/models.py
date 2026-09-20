import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Only these three kinds of uploads are accepted.
ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg']

TAG_CHOICES = [
    ('project', 'Project'),
    ('study', 'Study'),
    ('personal', 'Personal'),
]


class Note(models.Model):
    subject = models.CharField(max_length=200)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='project')

    # A note can be plain text, an uploaded file, or both.
    content = models.TextField(blank=True)
    file = models.FileField(
        upload_to='notes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)],
        help_text='PDF, JPG or JPEG only.',
    )

    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_notes')
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('note-detail', kwargs={'pk': self.pk})

    @property
    def extension(self):
        if not self.file:
            return ''
        return os.path.splitext(self.file.name)[1].lower().lstrip('.')

    @property
    def is_pdf(self):
        return self.extension == 'pdf'

    @property
    def is_image(self):
        return self.extension in ('jpg', 'jpeg')

    @property
    def kind(self):
        """Label shown on the note card."""
        if self.is_pdf:
            return 'PDF'
        if self.is_image:
            return 'Image'
        return 'Text'
