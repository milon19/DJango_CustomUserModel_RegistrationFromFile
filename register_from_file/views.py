import csv, random, string
import os
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.conf import settings
from django.contrib.auth import get_user_model

def handle_uploaded_file(f):
    base = settings.BASE_DIR
    with open(base + '/register_from_file/files/user.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return redirect('view_file')
        else:
            form = UploadFileForm()
        return render(request, 'register_with_file/upload_file.html', {'form': form})
    else:
        return render(request, 'register_with_file/upload_file_fail.html')


def random_password_generator(length=8):
    char = string.ascii_letters
    digit = string.digits
    pass_char = char + digit
    return ''.join(random.choice(pass_char) for i in range(length))


def ViewUploadFile(request):
    base = settings.BASE_DIR
    file = base + '/register_from_file/files/user.csv'
    if os.path.exists(file):
        users = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                password = random_password_generator(10)
                a_user = {
                    'email': row[0],
                    'name': row[1],
                    'password': password
                }
                users.append(a_user)

        context = {
            'users': users,
        }
        with open(base + '/register_from_file/files/user_with_password.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=users[0].keys())
            writer.writeheader()
            writer.writerows(users)
        return render(request, 'register_with_file/view-file.html', context)
    else:
        return redirect('upload_file')


def RegisterAllUser(request):
    base = settings.BASE_DIR
    file = base + '/register_from_file/files/user_with_password.csv'
    users = []
    if os.path.exists(file):
        with open(file) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                users.append(row)
                email = row['email']
                name = row['name']
                password = row['password']
                User = get_user_model()
                user = User()
                user.email = email
                user.name = name
                user.set_password(password)
                user.save()
                print('{} is registered successfully'.format(name))