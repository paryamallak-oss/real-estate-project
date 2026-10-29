from django.contrib.auth.models import User
from django.db import models


# ۱. مدل پروفایل برای تفکیک کاربر عادی و مشاور املاک
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='کاربر'
    )
    is_agent = models.BooleanField(
        default=False, verbose_name='مشاور املاک است؟'
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name='شماره تماس'
    )

    def __str__(self):
        role = 'مشاور املاک' if self.is_agent else 'کاربر عادی'
        return f'{self.user.username} ({role})'


# ۲. مدل اصلی ملک (Property) - شامل تمام نیازمندی‌های پروژه
class Property(models.Model):
    DEAL_CHOICES = (
        ('sale', 'فروش'),
        ('rent', 'رهن و اجاره'),
    )

    title = models.CharField(max_length=200, verbose_name='عنوان ملک')
    description = models.TextField(verbose_name='توضیحات کامل')
    deal_type = models.CharField(
        max_length=10, choices=DEAL_CHOICES, verbose_name='نوع معامله'
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='قیمت (تومان)'
    )
    area = models.PositiveIntegerField(verbose_name='متراژ (متر مربع)')
    rooms = models.PositiveIntegerField(verbose_name='تعداد اتاق')
    city = models.CharField(max_length=100, verbose_name='شهر')
    address = models.TextField(verbose_name='آدرس کامل')
    facilities = models.TextField(
        blank=True, null=True, verbose_name='امکانات (پارکینگ، آسانسور و...)'
    )
    image = models.ImageField(
        upload_to='properties/', blank=True, null=True, verbose_name='تصویر ملک'
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name='مشاور ثبت‌کننده',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ثبت آگهی'
    )

    def __str__(self):
        return f'{self.title} - {self.get_deal_type_display()} ({self.city})'


# ۳. مدل درخواست ملک (PropertyRequest) - برای ثبت درخواست کاربر برای ملک
class PropertyRequest(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name='ملک مورد نظر',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='property_requests',
        verbose_name='کاربر متقاضی',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ درخواست'
    )
    status = models.CharField(
        max_length=20, default='pending', verbose_name='وضعیت درخواست'
    )

    def __str__(self):
        return f'درخواست {self.user.username} برای {self.property.title}'


# ۴. مدل علاقه‌مندی‌ها (Favorite) - از بخش امتیازی پروژه
class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='کاربر',
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='ملک',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ افزودن به علاقه‌مندی‌ها'
    )

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f'{self.user.username} ⭐ {self.property.title}'


from django.db import models

# Create your models here.
