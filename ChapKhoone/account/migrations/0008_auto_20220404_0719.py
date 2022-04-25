# Generated by Django 3.2.10 on 2022-04-04 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20220319_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidencestamp',
            name='is_framework',
            field=models.BooleanField(blank=True, null=True, verbose_name='دارای کادر'),
        ),
        migrations.AlterField(
            model_name='evidencestamp',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='یادداشت'),
        ),
        migrations.AlterField(
            model_name='evidencestamp',
            name='stamp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.stamp', verbose_name='مهر مرتبط'),
        ),
        migrations.AlterField(
            model_name='evidencestamp',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری'),
        ),
        migrations.AlterField(
            model_name='stamp',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='موجودی انبار'),
        ),
    ]
