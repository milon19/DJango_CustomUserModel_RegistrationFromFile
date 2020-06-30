from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user