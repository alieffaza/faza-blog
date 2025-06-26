from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import requests

def edit_auth0_profile(request):
    userinfo = request.session.get('user')
    if not userinfo:
        return redirect('/auth/login/')

    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_email = request.POST.get('email')
        user_id = userinfo['sub']

        # Dapatkan Management API token
        token_url = f'https://{settings.AUTH0_DOMAIN}/oauth/token'
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': settings.AUTH0_CLIENT_ID,
            'client_secret': settings.AUTH0_CLIENT_SECRET,
            'audience': f'https://{settings.AUTH0_DOMAIN}/api/v2/'
        }
        token_resp = requests.post(token_url, json=token_data)
        mgmt_token = token_resp.json().get('access_token')

        # Update user di Auth0
        headers = {'Authorization': f'Bearer {mgmt_token}', 'Content-Type': 'application/json'}
        patch_data = {}
        if new_name: patch_data['name'] = new_name
        if new_email: patch_data['email'] = new_email
        resp = requests.patch(
            f'https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_id}',
            json=patch_data,
            headers=headers
        )
        if resp.status_code == 200:
            messages.success(request, 'Profil berhasil diperbarui. Silakan login ulang untuk melihat perubahan.')
            request.session['user']['name'] = new_name
            request.session['user']['email'] = new_email
        else:
            messages.error(request, 'Gagal memperbarui profil.')
        return redirect('edit_auth0_profile')

    return render(request, 'edit_auth0_profile.html', {
        'user': userinfo
    }) 