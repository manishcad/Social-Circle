# Generated by Django 4.1.4 on 2022-12-20 04:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
