from django.shortcuts import render, get_object_or_404, redirect
from .models import Artikel, Category, Komentar, Tag
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import get_user_model
import os
from urllib.parse import urlencode
from jose import jwt
import requests
from django.conf import settings
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

# Create your views here.

def index(request):
    artikels = Artikel.objects.all()
    artikel_terbaru = Artikel.objects.order_by('-tanggal')[:3]
    articles = Artikel.objects.exclude(gambar_judul='').exclude(gambar_judul=None)
    return render(request, 'pages/index.html', {
        'artikels': artikels,
        'artikel_terbaru': artikel_terbaru,
        'articles': articles,
    })

@cache_page(300)
def daftar_artikel(request):
    from .models import Tag
    sort = request.GET.get('sort', 'tanggal')
    order = request.GET.get('order', 'desc')
    tag_filter = request.GET.get('tag')
    q = request.GET.get('q', '')
    artikel = Artikel.objects.select_related('penulis', 'category').prefetch_related('tags').all()
    if tag_filter:
        artikel = artikel.filter(tags__name=tag_filter)
    if q:
        artikel = artikel.filter(Q(judul__icontains=q) | Q(isi__icontains=q))
    # Sorting hanya tanggal
    if order == 'asc':
        artikel = artikel.order_by('tanggal')
    else:
        artikel = artikel.order_by('-tanggal')
    # Pagination
    paginator = Paginator(artikel, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Ambil 4 tag terpopuler
    tags = Tag.objects.annotate(num_artikel=Count('artikels')).order_by('-num_artikel')[:4]
    sort_options = [
        {'label': 'Terbaru', 'order': 'desc'},
        {'label': 'Terlama', 'order': 'asc'},
    ]
    return render(request, 'pages/artikel_list.html', {
        'artikel': page_obj.object_list,
        'page_obj': page_obj,
        'tags': tags,
        'sort_options': sort_options,
        'selected_order': order,
        'selected_tag': tag_filter,
        'q': q,
    })

@cache_page(300)
def detail_artikel(request, pk):
    artikel = get_object_or_404(Artikel.objects.select_related('penulis', 'category').prefetch_related('tags', 'komentar__user'), pk=pk)
    tags = artikel.tags.all()
    related = Artikel.objects.filter(tags__in=tags).exclude(pk=artikel.pk).distinct().select_related('penulis', 'category').prefetch_related('tags')[:2]
    populer = Artikel.objects.annotate(num_komentar=Count('komentar')).order_by('-num_komentar', '-tanggal').select_related('penulis', 'category').prefetch_related('tags')[:2]
    komentar_list = artikel.komentar.select_related('user').all()
    # Navigasi prev/next
    try:
        prev_artikel = artikel.get_previous_by_tanggal()
    except Artikel.DoesNotExist:
        prev_artikel = None
    try:
        next_artikel = artikel.get_next_by_tanggal()
    except Artikel.DoesNotExist:
        next_artikel = None
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
    return render(request, 'pages/detail_artikel.html', {
        'artikel': artikel,
        'related_artikels': related,
        'populer_artikels': populer,
        'komentar_list': komentar_list,
        'prev_artikel': prev_artikel,
        'next_artikel': next_artikel,
    })

def tentang(request):
    return render(request, 'pages/tentang.html')

def galeri(request):
    articles_with_images = Artikel.objects.exclude(gambar_judul='').exclude(gambar_judul=None)
    paginator = Paginator(articles_with_images, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/galeri.html', {'articles': page_obj.object_list, 'page_obj': page_obj})

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    nama_lengkap = forms.CharField(label='Nama Lengkap', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Kata Sandi'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ulangi Kata Sandi'})

    class Meta:
        model = User
        fields = ['nama_lengkap', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email sudah digunakan.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        nama_lengkap = self.cleaned_data['nama_lengkap']
        parts = nama_lengkap.strip().split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
        user.username = user.email  # gunakan email sebagai username
        if commit:
            user.save()
        return user

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Kata Sandi', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kata Sandi'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError('Email atau password salah.')
            from django.contrib.auth import authenticate
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError('Email atau password salah.')
            self.user = user
        return self.cleaned_data
    def get_user(self):
        return getattr(self, 'user', None)

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = EmailLoginForm()
    return render(request, 'pages/login.html', {'form': form})

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
    return render(request, 'admin/admin_dashboard.html', {'users': users, 'artikels': artikels})

@login_required(login_url='login')
def penulis_dashboard(request):
    artikels = Artikel.objects.filter()
    return render(request, 'pages/penulis_dashboard.html', {'artikels': artikels})

@login_required(login_url='login')
def user_profile(request):
    return render(request, 'pages/user_profile.html')

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
    return render(request, 'admin/admin_users.html', {'users': users, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})

class ArtikelForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Artikel
        fields = ['judul', 'isi', 'gambar_judul', 'tags']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Judul Artikel'}),
            'gambar_judul': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'judul': 'Judul',
            'isi': 'Isi',
            'gambar_judul': 'Gambar Judul',
            'tags': 'Tag',
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
            form = ArtikelForm(request.POST, request.FILES)
            if form.is_valid():
                artikel = form.save(commit=False)
                artikel.penulis = request.user  # Set penulis ke user yang sedang login
                artikel.save()
                form.save_m2m()  # Untuk tags dan relasi many-to-many lain
                messages.success(request, 'Artikel berhasil ditambahkan.')
                return redirect('admin_artikels')
        elif 'edit' in request.POST:
            artikel = get_object_or_404(Artikel, id=request.POST.get('edit_id'))
            edit_form = ArtikelForm(request.POST, request.FILES, instance=artikel)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Artikel berhasil diubah.')
                return redirect('admin_artikels')
        elif 'delete' in request.POST:
            artikel = get_object_or_404(Artikel, id=request.POST.get('delete_id'))
            artikel.delete()
            messages.success(request, 'Artikel berhasil dihapus.')
            return redirect('admin_artikels')
    return render(request, 'admin/admin_artikels.html', {'artikels': artikels, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})

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
    return render(request, 'admin/admin_categories.html', {'categories': categories, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})

class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ['artikel', 'user', 'isi']
        widgets = {
            'artikel': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'isi': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Isi Komentar'}),
        }
        labels = {
            'artikel': 'Artikel',
            'user': 'User',
            'isi': 'Isi Komentar',
        }

@login_required(login_url='login')
def admin_komentar(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    komentars = Komentar.objects.select_related('artikel', 'user').all()
    form = None
    edit_form = None
    add_mode = request.GET.get('add') == '1'
    edit_id = request.GET.get('edit')
    if add_mode:
        form = KomentarForm()
    if edit_id:
        komentar = get_object_or_404(Komentar, id=edit_id)
        edit_form = KomentarForm(instance=komentar)
    if request.method == 'POST':
        if 'add' in request.POST:
            form = KomentarForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Komentar berhasil ditambahkan.')
                return redirect('admin_komentar')
        elif 'edit' in request.POST:
            komentar = get_object_or_404(Komentar, id=request.POST.get('edit_id'))
            edit_form = KomentarForm(request.POST, instance=komentar)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Komentar berhasil diubah.')
                return redirect('admin_komentar')
        elif 'delete' in request.POST:
            komentar = get_object_or_404(Komentar, id=request.POST.get('delete_id'))
            komentar.delete()
            messages.success(request, 'Komentar berhasil dihapus.')
            return redirect('admin_komentar')
    return render(request, 'admin/admin_komentar.html', {'komentars': komentars, 'form': form, 'edit_form': edit_form, 'edit_id': edit_id, 'add_mode': add_mode})

def auth0_login(request):
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
        'scope': 'openid profile email',
        'audience': f'https://{settings.AUTH0_DOMAIN}/userinfo',
    }
    return redirect(f'https://{settings.AUTH0_DOMAIN}/authorize?' + urlencode(params))

def auth0_callback(request):
    code = request.GET.get('code')
    token_url = f'https://{settings.AUTH0_DOMAIN}/oauth/token'
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
    }
    token_headers = {'content-type': 'application/x-www-form-urlencoded'}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    tokens = token_response.json()
    id_token = tokens.get('id_token')
    userinfo_url = f'https://{settings.AUTH0_DOMAIN}/userinfo'
    userinfo_response = requests.get(userinfo_url, headers={'Authorization': f'Bearer {tokens.get("access_token")}'})
    userinfo = userinfo_response.json()
    request.session['user'] = userinfo
    return redirect('/')

def auth0_logout(request):
    request.session.flush()
    return redirect(f'https://{settings.AUTH0_DOMAIN}/v2/logout?client_id={settings.AUTH0_CLIENT_ID}&returnTo=https://alieffazaumkt.pythonanywhere.com/')

def artikel_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    artikel = Artikel.objects.filter(tags=tag).order_by('-tanggal')
    return render(request, 'pages/artikel_list.html', {'artikel': artikel, 'filter_tag': tag})

def custom_bad_request(request, exception):
    return render(request, 'error/400.html', status=400)

def custom_permission_denied(request, exception):
    return render(request, 'error/403.html', status=403)

def custom_page_not_found(request, exception):
    return render(request, 'error/404.html', status=404)

def custom_server_error(request):
    return render(request, 'error/500.html', status=500)
