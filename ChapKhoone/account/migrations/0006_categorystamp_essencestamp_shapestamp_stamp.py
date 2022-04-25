# Generated by Django 3.2.10 on 2022-03-17 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20220317_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام دسته بندی مهر')),
            ],
        ),
        migrations.CreateModel(
            name='EssenceStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='رنگ جوهر مهر')),
            ],
        ),
        migrations.CreateModel(
            name='ShapeStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='شکل مهر')),
            ],
        ),
        migrations.CreateModel(
            name='Stamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='اسم مهر')),
                ('image', models.ImageField(upload_to='uploads/stamp', verbose_name='عکس مهر')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت مهر')),
                ('height', models.PositiveIntegerField(verbose_name='ارتفاع')),
                ('width', models.PositiveIntegerField(verbose_name='عرض')),
                ('length', models.PositiveIntegerField(verbose_name='طول')),
                ('is_bung', models.BooleanField(verbose_name='دارای درپوش')),
                ('company_name', models.CharField(max_length=50, verbose_name='شرکت سازنده')),
                ('producer_country', models.CharField(max_length=50, verbose_name='کشور مبدا')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.categorystamp', verbose_name='دسته بندی مهر')),
                ('essence_color', models.ManyToManyField(to='account.EssenceStamp', verbose_name='رنگ جوهر')),
                ('shape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.shapestamp', verbose_name='شکل مهر')),
            ],
        ),
    ]