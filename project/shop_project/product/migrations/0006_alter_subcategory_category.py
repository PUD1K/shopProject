# Generated by Django 4.0.4 on 2022-04-30 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='product.category'),
        ),
    ]