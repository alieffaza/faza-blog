# Generated by Django 5.2.3 on 2025-06-26 09:09

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_artikel_gambar_judul'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='isi',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
