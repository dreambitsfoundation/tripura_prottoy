# Generated by Django 2.2.4 on 2020-02-11 12:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0010_articlesmodel_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tall_image_id', models.TextField(default='')),
                ('tall_image_secure_url', models.TextField(default='')),
                ('wide_image_id', models.TextField(default='')),
                ('wide_image_secure_url', models.TextField(default='')),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
