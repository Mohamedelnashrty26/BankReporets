# Generated by Django 4.0.10 on 2024-01-22 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_section_related_sub_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='departments',
        ),
    ]
