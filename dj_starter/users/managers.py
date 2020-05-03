from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """Creates and saves a User with the given email and password."""
        if email is None:
            raise TypeError('Users must have a email.')
        if password is None:
            raise TypeError('Users must have a password.')
        
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a User with the given email and password and
        makes the user as super user."""
        if email is None:
            raise TypeError('Superusers must have a email.')
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
