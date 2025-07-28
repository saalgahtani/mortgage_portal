import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import FileResponse, Http404


# Login View
def bank_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('bank_upload')  # redirect to upload after login
    else:
        form = AuthenticationForm()
    return render(request, 'src_gateway/login.html', {'form': form})


# Bank Upload View
@login_required
def bank_upload(request):
    bank_username = request.user.username
    bank_folder = os.path.join('secure_files', bank_username)
    os.makedirs(bank_folder, exist_ok=True)

    if request.method == 'POST' and request.FILES.get('mortgage_file'):
        file = request.FILES['mortgage_file']
        fs = FileSystemStorage(location=bank_folder)
        fs.save(file.name, file)
        messages.success(request, f"{file.name} uploaded successfully.")

    uploaded_files = os.listdir(bank_folder) if os.path.exists(bank_folder) else []
    return render(request, 'src_gateway/bank_upload.html', {'files': uploaded_files})


# SRC Download Portal
@login_required
def src_portal(request):
    all_folders = os.listdir('secure_files') if os.path.exists('secure_files') else []
    files = []
    for folder in all_folders:
        folder_path = os.path.join('secure_files', folder)
        if os.path.isdir(folder_path):
            for f in os.listdir(folder_path):
                files.append((folder, f))
    return render(request, 'src_gateway/src_portal.html', {'files': files})


# Secure Download View
@login_required
def secure_download(request, bank_name, filename):
    file_path = os.path.join('secure_files', bank_name, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found")
