# Generated by Django 4.2.16 on 2024-12-07 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0011_alter_ads_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ads_images'),
        ),
        migrations.AddField(
            model_name='ads',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='ads_videos'),
        ),
    ]
