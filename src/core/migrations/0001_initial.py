# Generated by Django 2.1.7 on 2019-03-15 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_update_default_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registration', to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('number', models.IntegerField(unique=True)),
                ('active', models.BooleanField(default=True)),
                ('checkin', models.DateField()),
                ('checkout', models.DateField()),
                ('occupancy', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
            ],
        ),
        migrations.AddField(
            model_name='conferenceregistration',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registrations', to='core.Reservation'),
        ),
        migrations.AlterModelOptions(
            name='conferenceregistration',
            options={'verbose_name': 'Registration', 'verbose_name_plural': 'Registrations'},
        ),
    ]
