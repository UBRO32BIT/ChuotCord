# Generated by Django 4.2.4 on 2023-09-30 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_invite_string_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='messagegroup',
            name='chat_messag_group_i_625459_idx',
        ),
        migrations.AlterField(
            model_name='invite',
            name='string',
            field=models.CharField(default='YLNJebtGqV', editable=False, max_length=10, unique=True),
        ),
    ]
