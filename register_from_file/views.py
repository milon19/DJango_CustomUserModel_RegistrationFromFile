import os
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UploadFileForm
from .utils import *

csv_users = UnregisterUsers()


def upload_file(request):
    if csv_users.is_created:
        return redirect('view_file')

    if request.user.is_admin:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return redirect('view_file')
        else:
            form = UploadFileForm()
        csv_users.clear_data()
        return render(request, 'register_with_file/upload_file.html', {'form': form})
    else:
        return render(request, 'register_with_file/upload_file_fail.html')


def ViewUploadFile(request):
    if not os.path.exists(user_file):
        return redirect('upload_file')

    if not csv_users.is_created:
        with open(user_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                a_user = {
                    'email': row[0],
                    'name': row[1],
                }
                csv_users.add_user(a_user)
        csv_users.created()

    context = {
        'users': csv_users.get_user_list(),
        'export': csv_users.is_exported
    }
    return render(request, 'register_with_file/view-file.html', context)


def RegisterAllUser(request):
    if not csv_users.is_created:
        return redirect('upload_file')

    if csv_users.is_registered:
        return redirect('view_file')

    csv_users.set_password()
    csv_users.export_csv()
    csv_users.register()
    users = csv_users.get_user_list()

    context = {
        'users': users,
        'no_users': csv_users.total_users(),
        'export': csv_users.is_exported
    }

    return render(request, 'register_with_file/registration_complete.html', context)


def ExportCSV(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['email', 'name', 'password'])
    with open(user_file_with_password) as csv_file:
        users = csv.DictReader(csv_file)
        print(users)
        for user in users:
            print(user.values())
            writer.writerow(user.values())

    if os.path.exists(user_file):
        os.remove(user_file)
    if os.path.exists(user_file_with_password):
        os.remove(user_file_with_password)
    csv_users.clear_data()
    response['Content-Disposition'] = 'attachment; filename="user.csv"'
    return response
