from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('tentang/', views.tentang, name='tentang'),
    path('galeri/', views.galeri, name='galeri'),
    path('artikel/', views.daftar_artikel, name='daftar_artikel'),
    path('artikel/<int:pk>/', views.detail_artikel, name='detail_artikel'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
    path('admin-dashboard/artikels/', views.admin_artikels, name='admin_artikels'),
    path('admin-dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('admin-dashboard/komentar/', views.admin_komentar, name='admin_komentar'),
    path('penulis-dashboard/', views.penulis_dashboard, name='penulis_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('auth/login/', views.auth0_login, name='auth0_login'),
    path('auth/callback/', views.auth0_callback, name='auth0_callback'),
    path('auth/logout/', views.auth0_logout, name='auth0_logout'),
    path('tag/<str:tag_name>/', views.artikel_by_tag, name='artikel_by_tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'main.views.custom_bad_request'
handler403 = 'main.views.custom_permission_denied'
handler404 = 'main.views.custom_page_not_found'
handler500 = 'main.views.custom_server_error'   