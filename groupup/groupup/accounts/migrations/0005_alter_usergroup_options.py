# Generated by Django 4.0.2 on 2022-02-17 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_groupupuser_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergroup',
            options={'permissions': (('group_admin', 'Create and respond to group matches'),)},
        ),
    ]