# Generated by Django 4.1.7 on 2023-03-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0003_imagesample_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesample',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
