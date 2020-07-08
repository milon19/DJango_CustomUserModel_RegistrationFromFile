import csv
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model

base = settings.BASE_DIR
user_file = base + '/register_from_file/files/user.csv'
user_file_with_password = base + '/register_from_file/files/user_with_password.csv'


def random_password_generator(length=8):
    char = string.ascii_letters
    digit = string.digits
    pass_char = char + digit
    return ''.join(random.choice(pass_char) for i in range(length))


class UnregisterUsers:
    def __init__(self):
        self.users = []
        self.is_created = False
        self.is_setPassword = False
        self.is_exported = False
        self.is_registered = False
        self.is_save = False

    def add_user(self, user):
        self.users.append(user)

    def get_user_list(self):
        return self.users

    def set_password(self):
        if not self.is_setPassword:
            for user in self.users:
                password = random_password_generator(10)
                a_user = {
                    'password': password
                }
                user.update(a_user)
            self.is_setPassword = True

    def export_csv(self):
        if not self.is_exported:
            with open(user_file_with_password, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.users[0].keys())
                writer.writeheader()
                writer.writerows(self.users)
            self.is_exported = True

    def created(self):
        self.is_created = True

    def total_users(self):
        return len(self.users)

    def register(self):
        if not self.is_registered:
            for a_user in self.users:
                User = get_user_model()
                user = User()
                user.email = a_user['email']
                user.name = a_user['name']
                user.set_password(a_user['password'])
                user.save()
            self.is_registered = True

    def clear_data(self):
        self.users = []
        self.is_created = False
        self.is_setPassword = False
        self.is_exported = False
        self.is_registered = False
        self.is_save = False


def handle_uploaded_file(f):
    with open(user_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
