# Generated by Django 5.0.6 on 2024-12-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0002_alter_review_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.CharField(default='', max_length=100),
        ),
    ]
