from django.db import models

# Create your models here.

class Artikel(models.Model):
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.judul

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Komentar(models.Model):
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE, related_name='komentar')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    isi = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tanggal']

    def __str__(self):
        return f"Komentar oleh {self.user.username} pada {self.artikel.judul}"

