from datetime import datetime
import random
from unicodedata import category
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import ugettext as _
import pyotp
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation




class UserManager(BaseUserManager):
   
    def create_user(self, username, email, phone, password, **extra_fields):
        """
        Create and save a User with the given email, phone number and password.
        """
        if not email:
            raise ValueError('ایمیل باید وارد شود')
        if not phone:
            raise ValueError('شماره همراه باید وارد شود')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, username, email, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, phone number and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, phone, password, **extra_fields)
    
    
    
    
    
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + str(random.randint(0, 12000))
    return unique_slug






class Country(models.Model):
    name = models.CharField(_("name of country"), max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(_("name of city"), max_length=50)
    country = models.ForeignKey(Country, verbose_name=_("country of city"), on_delete=models.CASCADE)


    def __str__(self):
        return self.name




class CustomUser(AbstractUser):
    phone_regex = RegexValidator( regex = '^9\d{9}$', message ="شماره همراه باید به فرمت (9xxxxxxxxx) وارد شود.")
    phone = models.CharField(_('شماره همراه'),validators =[phone_regex], max_length=10, unique=True,null=True)
    email = models.EmailField(_('آدرس ایمیل'), unique=True)
    REQUIRED_FIELDS = ['email', 'phone']
    is_verified = models.BooleanField('تایید شد', default=False, help_text='Designates whether this user has verified phone')
    key = models.CharField(max_length=100, unique=True, blank=True)



    objects = UserManager()  


    def __str__(self):
        return f'{self.phone} / {self.username}' 
    
    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        #Here we are using Time Based OTP. The interval is 60 seconds.
        #otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.key, interval=300)
        return t.verify(provided_otp)
    
    
        

class Profile(models.Model):
    Male= 'male'
    Female= 'fmle'
    STATUS= [
        (Male, 'مذکر'),
        (Female, 'مونث'),
    ]
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")
    first_name = models.CharField(_("نام"), max_length=50)
    last_name = models.CharField(_("نام خانوادگی"), max_length=50)
    invite_code = models.CharField(_("کد معرفی "), max_length=20, unique=True)
    description = models.TextField(_("بیوگرافی"), null=True, blank=True)
    address = models.CharField(_("آدرس"),max_length=30,blank=True)
    date_joined = models.DateTimeField(_("تاریخ پیوستن"),auto_now_add=True)
    age = models.PositiveIntegerField(_("سن"),null=True, blank=True)
    sexuality = models.CharField(_("جنسیت"), max_length=4, choices=STATUS, default=Male)
    updated_on = models.DateTimeField(_("تاریخ ویرایش"),auto_now=True)
    image = models.ImageField("عکس کاربر",upload_to='uploads/profile', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    city = models.ForeignKey(City, verbose_name=_("شهر"), on_delete=models.CASCADE, null=True, blank=True)
    use_invite_code = models.BooleanField(_("استفاده از کد معرف"), default=False)
    

    def __str__(self):
        return self.user.username
    
    

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="wallet")
    date_create = models.DateTimeField(_("تاریخ ایجاد"), auto_now=False, auto_now_add=True)
    cash = models.PositiveIntegerField(_("موجودی کیف پول"), default=0)

    def __str__(self):
        return f'{self.user.username} / {self.cash}'
   
   
   
    
    
class Transaction(models.Model):
    TYPE = (("1", "واریز"), ("2", "برداشت"))
    wallet = models.OneToOneField(Wallet, verbose_name=_("کیف پول"), on_delete=models.CASCADE)
    date_transaction = models.DateTimeField(_("تاریخ تراکنش"), auto_now=True, auto_now_add=False)
    type = models.CharField(_("نوع تراکنش"), max_length=1, choices=TYPE)
    amount = models.PositiveIntegerField(_("مبلغ تراکنش"))
    
    def __str__(self):
        return f'{self.wallet} / {self.type}'
    
    
    
    
class Service(models.Model):
    name = models.CharField(_("نام سرویس"), max_length=50)
    slug = models.SlugField(_("اسلاگ"), blank=True)
    available = models.BooleanField(_("در دسترس"))
    short_description = models.CharField(_("توضیح کوتاه "), max_length=50)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse("services", kwargs={"slug": self.slug})
    
    
class CategoryStamp(models.Model):
    name = models.CharField(_("نام دسته بندی مهر"), max_length=50)
    slug = models.SlugField(_("اسلاگ"), blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("stamp-category", kwargs={"slug": self.slug})
    
    
    
    
    
class EssenceStamp(models.Model):
    name = models.CharField(_("رنگ جوهر مهر"), max_length=50)
    slug = models.SlugField(_("اسلاگ"), blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name}'



class ShapeStamp(models.Model):
    name = models.CharField(_("شکل مهر"), max_length=50)
    slug = models.SlugField(_("اسلاگ"), blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}'
   
    
    
    
    
    
    
    
class Cart(models.Model):
    Paid = 'PID'
    Confirmed = 'CFD'
    Canceled = 'CNL'
    Pending = 'PND'
    CHOICES = [(Paid, 'پرداخت شده'),(Canceled, 'کنسل شده'),(Pending, 'در حال پردازش'), (Confirmed, 'تایید شده')]
    status_payment = models.CharField(_("وضعیت پرداخت"),max_length=3,choices= CHOICES, default=Pending)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    order_number = models.CharField(_("شماره سفارش"),max_length=23, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(_("تاریخ ایجاد"),auto_now_add=True)
    paid_amount = models.PositiveIntegerField(_("قیمت پرداختی"), blank=True, null=True)
    paid_date = models.DateTimeField(_("تاریخ پرداخت"),null=True, blank=True)
    cartitem = GenericRelation('account.cartitem')

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'{self.user}/{self.status_payment}/{self.order_number}'

    def save(self, *args, **kwargs):
        final_price = 0
        items = self.cartitem_set.all()
        for item in items:
            price = item.price
            quantity = item.quantity
            final_price += price * quantity
        self.paid_amount = final_price
        if not self.order_number:
            self.order_number = str(get_random_string(length=2)) + str(random.randint(1000, 9999)) + str(self.pk)
        if self.status_payment == 'PID':
            self.paid_date = datetime.now()
        super().save(*args, **kwargs)


class Stamp(models.Model):
    name = models.CharField(_("اسم مهر"), max_length=50)
    image = models.ImageField(_("عکس مهر"), upload_to='uploads/stamp', height_field=None, width_field=None, max_length=None)
    price = models.PositiveIntegerField(_("قیمت مهر"))
    category = models.ForeignKey(CategoryStamp, verbose_name=_("دسته بندی مهر"), on_delete=models.CASCADE)
    essence_color = models.ManyToManyField(EssenceStamp, verbose_name=_("رنگ جوهر"))
    height = models.PositiveIntegerField(_("ارتفاع"))
    width = models.PositiveIntegerField(_("عرض"))
    length = models.PositiveIntegerField(_("طول"))
    shape = models.ForeignKey(ShapeStamp, verbose_name=_("شکل مهر"), on_delete=models.CASCADE)
    is_bung = models.BooleanField(_("دارای درپوش"))
    company_name = models.CharField(_("شرکت سازنده"), max_length=50)
    producer_country = models.CharField(_("کشور مبدا"), max_length=50)
    description = models.TextField(_("توضیحات"))
    slug = models.SlugField(_("اسلاگ"), blank=True)
    stock = models.PositiveIntegerField(_("موجودی انبار"))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}/ {self.shape}'
    
    
    def get_absolute_url(self):
        return reverse("stamp-detail", kwargs={"slug": self.slug}) 
    
    
    

class CartItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("شماره شی"), blank=True)
    items = GenericForeignKey('content_type', 'object_id')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.PositiveIntegerField(blank=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.items.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.items}/{self.cart}'






    
    
    
    
    
    
    
    
    
class EvidenceStamp(models.Model):
    stamp = models.ForeignKey(Stamp, verbose_name=_("مهر مرتبط"), on_delete=models.DO_NOTHING, null=True, blank=True)
    evidence = models.ImageField(_("مدرک اصلی"), upload_to='uploads/evidence-stamp')
    evidence2 = models.ImageField(_("مدرک اصلی ۲"), upload_to='uploads/evidence-stamp', null=True, blank=True)
    sketch_stamp = models.ImageField(_("طرح مهر"), upload_to='uploads/sketch-stamp')
    note = models.TextField(_("یادداشت"), null=True, blank=True)
    is_framework = models.BooleanField(_("دارای کادر"), null=True, blank=True)
    user = models.ForeignKey(CustomUser, verbose_name=_("مشتری"), on_delete=models.CASCADE, null=True, blank=True)
    is_confirmed = models.BooleanField(_("تایید شده"), null=True, blank=True)
