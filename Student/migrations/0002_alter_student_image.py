# Generated by Django 5.0.6 on 2024-12-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.CharField(default='', max_length=100),
        ),
    ]