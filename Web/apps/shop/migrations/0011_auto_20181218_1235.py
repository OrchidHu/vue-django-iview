# Generated by Django 2.1.2 on 2018-12-18 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20181217_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockrecord',
            name='good_id',
        ),
        migrations.AddField(
            model_name='stockrecord',
            name='good',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shop.Good', verbose_name='商品'),
            preserve_default=False,
        ),
    ]
