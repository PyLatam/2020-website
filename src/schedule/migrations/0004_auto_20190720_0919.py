# Generated by Django 2.1.9 on 2019-07-20 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_talk_is_keynote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='title',
            new_name='title_en',
        ),
        migrations.AddField(
            model_name='event',
            name='title_es',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
