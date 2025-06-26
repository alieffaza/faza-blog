from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('tentang/', views.tentang, name='tentang'),
    path('galeri/', views.galeri, name='galeri'),
    path('artikel/', views.daftar_artikel, name='daftar_artikel'),
    path('<int:pk>/', views.detail_artikel, name='detail_artikel'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
    path('admin-dashboard/artikels/', views.admin_artikels, name='admin_artikels'),
    path('admin-dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('penulis-dashboard/', views.penulis_dashboard, name='penulis_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
]   