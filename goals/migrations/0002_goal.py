# Generated by Django 2.1.5 on 2019-01-06 17:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolution', models.TextField(null=True)),
                ('reason', models.TextField(null=True)),
                ('duration', models.DurationField(choices=[(datetime.timedelta(days=30), 'ONE MONTH'), (datetime.timedelta(days=90), 'THREE MONTHS')], null=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
