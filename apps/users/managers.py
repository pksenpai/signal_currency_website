from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone_number, country, password=None):
        if not username:
            raise ValueError("Users must have an username address")

        if not phone_number:
            raise ValueError("Users must have an phone number")
        
        if not country:
            raise ValueError("Phone Numbers must have an country code number")

        user = self.model(
            username=username,
            phone_number=phone_number,
            country=country,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, country, password=None):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            country=country,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
