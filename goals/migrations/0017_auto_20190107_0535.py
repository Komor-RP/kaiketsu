# Generated by Django 2.1.5 on 2019-01-07 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0016_goal_type_of'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='type_of',
            new_name='category',
        ),
    ]