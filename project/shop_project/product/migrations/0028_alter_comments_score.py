# Generated by Django 4.0.4 on 2023-05-09 10:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_alter_comments_options_alter_manufacturer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
