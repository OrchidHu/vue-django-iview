# Generated by Django 2.1.2 on 2018-11-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xyuser',
            name='avatar',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='driver/%Y/%m/%d', verbose_name='头像'),
        ),
    ]