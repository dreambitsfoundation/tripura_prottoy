# Generated by Django 2.2.4 on 2019-10-29 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_staticarticlemodel_staticcategorymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticcategorymodel',
            name='articles',
            field=models.ManyToManyField(to='administrator.StaticArticleModel'),
        ),
    ]
