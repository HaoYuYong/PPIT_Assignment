# Generated by Django 5.1.7 on 2025-04-16 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_workexperience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('skill', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='api.user', to_field='uid')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'db_table': 'skills',
                'ordering': ['-created_at'],
            },
        ),
    ]
