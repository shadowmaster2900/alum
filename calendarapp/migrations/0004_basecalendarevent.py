# Generated by Django 3.2.7 on 2023-09-07 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_auto_20230904_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCalendarEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
    ]
