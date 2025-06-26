from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

def index(request):
    artikels = Artikel.objects.all()
    artikel_terbaru = Artikel.objects.order_by('-tanggal')[:3]
    galeri_peek = [
        f'https://source.unsplash.com/400x300/?nature,water,{i}' for i in range(1, 7)
    ]
    return render(request, 'index.html', {
        'artikels': artikels,
        'artikel_terbaru': artikel_terbaru,
        'galeri_peek': galeri_peek,
    })

def daftar_artikel(request):
    artikel = Artikel.objects.all().order_by('-tanggal')
    return render(request, 'artikel_list.html', {'artikel': artikel})

def detail_artikel(request, pk):
    artikel = get_object_or_404(Artikel, pk=pk)
    komentar_list = artikel.komentar.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            isi = request.POST.get('isi')
            if isi:
                from .models import Komentar
                Komentar.objects.create(artikel=artikel, user=request.user, isi=isi)
                messages.success(request, 'Komentar berhasil ditambahkan.')
                return redirect('detail_artikel', pk=pk)
        else:
            messages.error(request, 'Anda harus login untuk berkomentar.')
            return redirect('login')
    return render(request, 'detail_artikel.html', {'artikel': artikel, 'komentar_list': komentar_list})

def tentang(request):
    return render(request, 'tentang.html')

def galeri(request):
    return render(request, 'galeri.html')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nama Pengguna'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Kata Sandi'})

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nama Pengguna'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Kata Sandi'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ulangi Kata Sandi'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.is_staff:
        return redirect('penulis_dashboard')
    else:
        return redirect('user_profile')

@login_required(login_url='login')
def admin_dashboard(request):
    users = User.objects.all()
    artikels = Artikel.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users, 'artikels': artikels})

@login_required(login_url='login')
def penulis_dashboard(request):
    artikels = Artikel.objects.filter()
    return render(request, 'penulis_dashboard.html', {'artikels': artikels})

@login_required(login_url='login')
def user_profile(request):
    return render(request, 'user_profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pengguna'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_staff': forms.CheckboxInput(),
            'is_superuser': forms.CheckboxInput(),
        }
        labels = {
            'username': 'Nama Pengguna',
            'email': 'Email',
            'is_staff': 'Penulis',
            'is_superuser': 'Admin',
        }

class UserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pengguna'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'is_staff': forms.CheckboxInput(),
            'is_superuser': forms.CheckboxInput(),
        }
        labels = {
            'username': 'Nama Pengguna',
            'email': 'Email',
            'is_staff': 'Penulis',
            'is_superuser': 'Admin',
        }

@login_required(login_url='login')
def admin_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    users = User.objects.all()
    form = None
    edit_form = None
    add_mode = request.GET.get('add') == '1'
    edit_id = request.GET.get('edit')
    if add_mode:
        form = UserForm()
    if edit_id:
        user = get_object_or_404(User, id=edit_id)
        edit_form = UserEditForm(instance=user)
    if request.method == 'POST':
        if 'add' in request.POST:
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User berhasil ditambahkan.')
                return redirect('admin_users')
        elif 'edit' in request.POST:
            user = get_object_or_404(User, id=request.POST.get('edit_id'))
            edit_form = UserEditForm(request.POST, instance=user)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'User berhasil diubah.')
                return redirect('admin_users')
        elif 'delete' in request.POST:
            user = get_object_or_404(User, id=request.POST.get('delete_id'))
            user.delete()
            messages.success(request, 'User berhasil dihapus.')
            return redirect('admin_users')
    return render(request, 'admin_users.html', {'users': users, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})

class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = ['judul', 'isi']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Artikel'}),
            'isi': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Isi Artikel', 'rows': 4}),
        }
        labels = {
            'judul': 'Judul',
            'isi': 'Isi',
        }

@login_required(login_url='login')
def admin_artikels(request):
    artikels = Artikel.objects.all()
    form = None
    edit_form = None
    add_mode = request.GET.get('add') == '1'
    edit_id = request.GET.get('edit')
    if add_mode:
        form = ArtikelForm()
    if edit_id:
        artikel = get_object_or_404(Artikel, id=edit_id)
        edit_form = ArtikelForm(instance=artikel)
    if request.method == 'POST':
        if 'add' in request.POST:
            form = ArtikelForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Artikel berhasil ditambahkan.')
                return redirect('admin_artikels')
        elif 'edit' in request.POST:
            artikel = get_object_or_404(Artikel, id=request.POST.get('edit_id'))
            edit_form = ArtikelForm(request.POST, instance=artikel)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Artikel berhasil diubah.')
                return redirect('admin_artikels')
        elif 'delete' in request.POST:
            artikel = get_object_or_404(Artikel, id=request.POST.get('delete_id'))
            artikel.delete()
            messages.success(request, 'Artikel berhasil dihapus.')
            return redirect('admin_artikels')
    return render(request, 'admin_artikels.html', {'artikels': artikels, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Kategori'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Deskripsi', 'rows': 2}),
        }

@login_required(login_url='login')
def admin_categories(request):
    categories = Category.objects.all()
    form = None
    edit_form = None
    add_mode = request.GET.get('add') == '1'
    edit_id = request.GET.get('edit')
    if add_mode:
        form = CategoryForm()
    else:
        form = CategoryForm()
    if edit_id:
        kategori = get_object_or_404(Category, id=edit_id)
        edit_form = CategoryForm(instance=kategori)
    if request.method == 'POST':
        if 'add' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Kategori berhasil ditambahkan.')
                return redirect('admin_categories')
        elif 'edit' in request.POST:
            kategori = get_object_or_404(Category, id=request.POST.get('edit_id'))
            edit_form = CategoryForm(request.POST, instance=kategori)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Kategori berhasil diubah.')
                return redirect('admin_categories')
        elif 'delete' in request.POST:
            kategori = get_object_or_404(Category, id=request.POST.get('delete_id'))
            kategori.delete()
            messages.success(request, 'Kategori berhasil dihapus.')
            return redirect('admin_categories')
    return render(request, 'admin_categories.html', {'categories': categories, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})
