# Generated by Django 5.1.4 on 2025-01-02 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_foodcategory_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodcategory',
            name='category_image',
            field=models.ImageField(null=True, upload_to='category_images'),
        ),
    ]
