# Generated by Django 4.0.4 on 2022-04-23 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('type', models.CharField(max_length=255)),
                ('processor', models.CharField(max_length=255)),
                ('videocart', models.CharField(max_length=255)),
                ('hdd', models.CharField(max_length=255)),
                ('ram', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
    ]
