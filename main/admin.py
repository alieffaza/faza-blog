from django.contrib import admin
from .models import Artikel, Category, Komentar
from django import forms
from ckeditor.widgets import CKEditorWidget

class ArtikelAdminForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = '__all__'

class ArtikelAdmin(admin.ModelAdmin):
    form = ArtikelAdminForm
    list_display = ('judul', 'tanggal')
    search_fields = ['judul', 'isi']
    list_filter = ('tanggal',)

class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Category
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name',)
    search_fields = ['name', 'description']

class KomentarAdmin(admin.ModelAdmin):
    list_display = ('artikel', 'user', 'tanggal')
    list_filter = ('tanggal', 'user')
    search_fields = ['isi', 'user__username', 'artikel__judul']

admin.site.register(Artikel, ArtikelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Komentar, KomentarAdmin)
