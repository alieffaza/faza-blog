from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Artikel, Category

admin.site.register(Artikel)
admin.site.register(Category)
