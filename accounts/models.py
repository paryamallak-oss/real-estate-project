from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
  # انتخاب نقش کاربر
  ROLE_CHOICES = (
      ('customer', 'مستأجر / خریدار (کاربر عادی)'),
      ('owner', 'مالک / مشاور املاک (آگهی‌دهنده)'),
  )

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  role = models.CharField(
      max_length=20,
      choices=ROLE_CHOICES,
      default='customer',
      verbose_name='نقش کاربر',
  )

  # اطلاعات احراز هویت
  phone_number = models.CharField(
      max_length=11, verbose_name='شماره موبایل', blank=True, null=True
  )
  national_code = models.CharField(
      max_length=10, verbose_name='کد ملی', blank=True, null=True
  )

  # وضعیت تایید توسط ادمین (مخصوص مالکین برای انتشار آگهی)
  is_verified = models.BooleanField(
      default=False, verbose_name='تایید شده توسط ادمین'
  )

  def __str__(self):
    return (
        f'{self.user.username} - {self.get_role_display()} -'
        f' {"تاییدشده" if self.is_verified else "در انتظار تایید"}'
    )