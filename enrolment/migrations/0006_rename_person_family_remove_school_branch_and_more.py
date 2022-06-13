# Generated by Django 4.0.5 on 2022-06-08 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enrolment', '0005_alter_student_residental_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Person',
            new_name='Family',
        ),
        migrations.RemoveField(
            model_name='school',
            name='branch',
        ),
        migrations.AddField(
            model_name='branch',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='enrolment.school'),
            preserve_default=False,
        ),
    ]