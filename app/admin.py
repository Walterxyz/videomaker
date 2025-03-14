from django.contrib import admin
from .models import Servidor, Expurgo, Slots

# Register your models here.

admin.site.register(Servidor)
admin.site.register(Expurgo)
admin.site.register(Slots)