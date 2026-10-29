from django.contrib import admin
from .models import Favorite, Profile, Property, PropertyRequest

admin.site.register(Profile)
admin.site.register(Property)
admin.site.register(PropertyRequest)
admin.site.register(Favorite)