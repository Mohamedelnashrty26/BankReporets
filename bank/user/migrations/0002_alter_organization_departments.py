# Generated by Django 4.0.10 on 2024-01-15 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='department', to='user.department'),
        ),
    ]
