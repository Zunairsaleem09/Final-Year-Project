from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(profile_edit)
admin.site.register([Product, Image])
admin.site.register(reserve)
admin.site.register(parking_detail)