# Generated by Django 3.2.10 on 2022-03-08 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='userrrr', max_length=50, verbose_name='نام'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='asasa', max_length=50, verbose_name='نام خانوادگی'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile', verbose_name='عکس کاربر'),
        ),
    ]
