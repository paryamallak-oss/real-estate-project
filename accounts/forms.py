from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile


class SignUpForm(UserCreationForm):
  # فیلدهای اضافه که در جدول User پیش‌فرض نیستند اما در UserProfile هستند
  email = forms.EmailField(required=True, label='ایمیل')
  role = forms.ChoiceField(
      choices=UserProfile.ROLE_CHOICES, label='نقش شما در سامانه'
  )
  phone_number = forms.CharField(max_length=11, label='شماره موبایل')
  national_code = forms.CharField(max_length=10, label='کد ملی')

  class Meta(UserCreationForm.Meta):
    model = User
    fields = UserCreationForm.Meta.fields + ('email',)

  def save(self, commit=True):
    # ابتدا کاربر اصلی را ذخیره می‌کنیم
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
      user.save()
      # سپس اطلاعات تکمیلی را در پروفایل کاربری ذخیره می‌کنیم
      profile, created = UserProfile.objects.get_or_create(user=user)
      profile.role = self.cleaned_data['role']
      profile.phone_number = self.cleaned_data['phone_number']
      profile.national_code = self.cleaned_data['national_code']
      profile.save()
    return user