# Generated by Django 2.1.9 on 2019-07-18 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='speaker',
            old_name='bio',
            new_name='bio_en',
        ),
        migrations.AddField(
            model_name='speaker',
            name='bio_es',
            field=models.TextField(blank=True),
        ),
    ]
