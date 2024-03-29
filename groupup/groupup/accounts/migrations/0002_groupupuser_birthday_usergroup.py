# Generated by Django 4.0.2 on 2022-02-11 15:00

from django.db import migrations, models
import django.db.models.deletion
import groupup.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupupuser',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=250)),
                ('num_of_members', models.IntegerField(default=1)),
                ('group_pic', models.ImageField(upload_to=groupup.accounts.models.group_image_path)),
                ('group_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_admin', to='accounts.groupupuser')),
                ('interests', models.ManyToManyField(to='accounts.Interest')),
                ('members', models.ManyToManyField(to='accounts.GroupUpUser')),
            ],
            options={
                'db_table': 'user_group',
            },
        ),
    ]
