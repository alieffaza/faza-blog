from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    isi = RichTextUploadingField()
    tanggal = models.DateField(auto_now_add=True)
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)
    gambar_judul = models.ImageField(upload_to='artikel_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='artikels')

    def __str__(self):
        return self.judul

class Komentar(models.Model):
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE, related_name='komentar')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isi = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tanggal']

    def __str__(self):
        return f"Komentar oleh {self.user.username} pada {self.artikel.judul}"

