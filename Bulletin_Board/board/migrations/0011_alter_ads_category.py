# Generated by Django 4.2.16 on 2024-12-06 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_alter_ads_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='board.category'),
        ),
    ]