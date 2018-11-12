# Generated by Django 2.1.2 on 2018-11-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='bar_id',
            field=models.CharField(max_length=30, unique=True, verbose_name='条码'),
        ),
        migrations.AlterField(
            model_name='good',
            name='supplier',
            field=models.CharField(blank=True, default='临时供应商', max_length=200, null=True, verbose_name='供货商'),
        ),
    ]
