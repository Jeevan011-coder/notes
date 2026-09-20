import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_note_author_remove_note_notes_note_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='pdf',
            new_name='file',
        ),
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(
                blank=True,
                null=True,
                help_text='PDF, JPG or JPEG only.',
                upload_to='notes/',
                validators=[django.core.validators.FileExtensionValidator(
                    allowed_extensions=['pdf', 'jpg', 'jpeg'])],
            ),
        ),
        migrations.AddField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='tag',
            field=models.CharField(
                choices=[('project', 'Project'), ('study', 'Study'), ('personal', 'Personal')],
                default='project', max_length=20),
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-date_posted']},
        ),
    ]
