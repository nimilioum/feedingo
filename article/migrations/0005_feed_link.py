# Generated by Django 3.2.7 on 2022-11-04 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_alter_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='link',
            field=models.URLField(default='https://fake.com', unique=True),
        ),
    ]