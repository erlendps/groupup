# Generated by Django 4.0.2 on 2022-03-10 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_usergroup_num_of_members'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergroup',
            options={},
        ),
        migrations.AddField(
            model_name='usergroup',
            name='admin_contact',
            field=models.EmailField(default='example@gmail.com', max_length=100),
        ),
        migrations.CreateModel(
            name='DateAvailable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connected_group', to='accounts.usergroup')),
            ],
        ),
    ]
