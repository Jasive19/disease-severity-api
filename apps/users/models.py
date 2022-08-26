from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    def _create_user(self, email, name, last_name, password, first_name, is_staff, is_superuser, is_admin, **extra_fields):
        user = self.model(
            name=name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_admin=is_admin,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, name, last_name, first_name, password=None, **extra_fields):
        return self._create_user(email, name, last_name, password, first_name, False, False, False, **extra_fields)

    def create_superuser(self, email, name, last_name, password=None, **extra_fields):
        return self._create_user(email, name, last_name, password, '', True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True,editable=False, default=uuid.uuid4, unique=True)
    email = models.EmailField('Correo Electrónico',max_length=255, unique=True,)
    name = models.CharField('Nombres', max_length=255)
    first_name = models.CharField('Apellido Materno', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellido Paterno', max_length=255, blank=True, null=True)
    image = models.ImageField('Imagen de perfil', max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    def __str__(self):
        return self.email

        # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
