# Generated by Django 4.2.1 on 2023-05-09 16:52

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_specifications_productshots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='best_seller',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Описание'),
        ),
    ]