# Generated by Django 2.1.2 on 2018-10-17 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0005_auto_20181017_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xyuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='姓'),
        ),
        migrations.AlterField(
            model_name='xyuser',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='名'),
        ),
    ]
