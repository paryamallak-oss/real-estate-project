from django.shortcuts import get_object_or_404, render
from .models import Property


# ویوی صفحه اصلی و لیست املاک
def property_list(request):
  properties = Property.objects.all().order_by('-created_at')
  context = {
      'properties': properties,
  }
  return render(request, 'properties/property_list.html', context)


# ویوی صفحه جزئیات یک ملک
def property_detail(request, pk):
  # ملک مورد نظر را بر اساس کلید اصلی (pk) پیدا می‌کند یا ارور 404 می‌دهد
  property_item = get_object_or_404(Property, pk=pk)
  context = {
      'property': property_item,
  }
  return render(request, 'properties/property_detail.html', context)