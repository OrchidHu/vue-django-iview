# Generated by Django 2.1.2 on 2018-12-12 08:00

import Utils.my_validators
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='XYUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MaxLengthValidator(30)], verbose_name='姓名')),
                ('gender', models.CharField(choices=[('boy', '男'), ('girl', '女')], default='boy', max_length=10, verbose_name='性别')),
                ('email', models.EmailField(blank=True, db_index=True, max_length=50, null=True, validators=[django.core.validators.EmailValidator()], verbose_name='邮箱地址')),
                ('phone', models.CharField(blank=True, db_index=True, max_length=15, null=True, validators=[Utils.my_validators.PhoneValidator()], verbose_name='手机号码')),
                ('id_number', models.CharField(blank=True, help_text='请输入18位有效身份证号码', max_length=80, null=True, validators=[Utils.my_validators.UserIDCardValidator()], verbose_name='身份证号')),
                ('avatar', models.ImageField(blank=True, max_length=200, null=True, upload_to='images/%Y/%m/%d', verbose_name='头像')),
                ('position', models.CharField(choices=[('boss', '老板'), ('manager', '管理员'), ('cashier', '收银员'), ('waiter', '服务员'), ('pullover', '送货员')], default='cashier', max_length=30, verbose_name='职位')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='最后一次登录')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='加入时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': '鑫意用户',
                'verbose_name_plural': '用户',
                'db_table': 'auth_user',
                'ordering': ['-id'],
                'permissions': (('boos', '老板'), ('manager', '管理员'), ('cashier', '收银员'), ('staff', '普通员工'), ('goods_manage', '商品管理'), ('sale_manage', '销售管理'), ('order_goods_manage', '进货管理'), ('stock_manage', '库存管理'), ('report_manage', '报表管理'), ('setting_manage', '设置管理')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
