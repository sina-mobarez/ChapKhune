# Generated by Django 3.2.10 on 2022-03-04 13:47

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='شماره همراه باید به فرمت (9xxxxxxxxx) وارد شود.', regex='^9\\d{9}$')], verbose_name='شماره همراه')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='آدرس ایمیل')),
                ('is_verified', models.BooleanField(default=False, help_text='Designates whether this user has verified phone', verbose_name='تایید شد')),
                ('key', models.CharField(blank=True, max_length=100, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of city')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name of country')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('cash', models.PositiveIntegerField(blank=True, null=True, verbose_name='موجودی کیف پول')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_transaction', models.DateTimeField(auto_now=True, verbose_name='تاریخ تراکنش')),
                ('type', models.CharField(choices=[('1', 'واریز'), ('2', 'برداشت')], max_length=1, verbose_name='نوع تراکنش')),
                ('amount', models.PositiveIntegerField(verbose_name='مبلغ تراکنش')),
                ('wallet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.wallet', verbose_name='کیف پول')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='بیوگرافی')),
                ('address', models.CharField(blank=True, max_length=30, verbose_name='آدرس')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پیوستن')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='سن')),
                ('sexuality', models.CharField(choices=[('male', 'مذکر'), ('fmle', 'مونث')], default='male', max_length=4, verbose_name='جنسیت')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/profile', verbose_name='عکس کاربر')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.city', verbose_name='شهر')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.country', verbose_name='country of city'),
        ),
    ]