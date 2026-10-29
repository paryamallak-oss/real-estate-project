from .forms import SignUpForm  # ایمپورت فرم سفارشی که ساختیم
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render


# ویوی ثبت‌نام کاربر جدید
def signup_view(request):
  if request.method == 'POST':
    form = SignUpForm(
        request.POST
    )  # استفاده از فرم سفارشی شامل موبایل، کد ملی و نقش
    if form.is_valid():
      user = form.save()
      login(request, user)  # کاربر بلافاصله بعد از ثبت‌نام وارد می‌شود
      messages.success(request, 'حساب کاربری شما با موفقیت ساخته شد!')
      return redirect('property_list')
  else:
    form = SignUpForm()
  return render(request, 'registration/signup.html', {'form': form})


# ویوی خروج از حساب
def logout_view(request):
  logout(request)
  messages.info(request, 'شما از حساب کاربری خود خارج شدید.')
  return redirect('property_list')
