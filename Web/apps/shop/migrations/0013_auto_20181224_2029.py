# Generated by Django 2.1.2 on 2018-12-24 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_examinestockrecord_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodpackage',
            old_name='package_price',
            new_name='sale_price',
        ),
    ]
