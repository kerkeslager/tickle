# Generated by Django 3.1.7 on 2021-02-25 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boulder',
            name='mountainproject',
            field=models.URLField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='mountainproject',
            field=models.URLField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
