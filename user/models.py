from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from .validators import PhoneValidator, validate_f_name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.KAFEDRA)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        DEKAN = 'dekan', 'Dekan'
        KAFEDRA = 'kafedra', 'Kafedra'
        USTOZ = 'ustoz', 'Ustoz'

    full_name = models.CharField(
        max_length=255,
        verbose_name='To‘liq ism',
        help_text="Iltimos, to‘liq ismingizni kiriting.",
        validators=[validate_f_name],
        blank=True,
        default=''
    )
    email = models.EmailField(unique=True)
    p_number = models.CharField(
        max_length=13,
        validators=[PhoneValidator()],
        verbose_name='Telefon raqam',
        help_text="Iltimos, raqamni to‘g‘ri kiriting. Masalan: +998123456789",
        blank=True,
        default=''
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USTOZ
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split(' ')[0] or self.email.split('@')[0]

    def is_kafedra(self):
        return self.role == self.Role.KAFEDRA

    def is_ustoz(self):
        return self.role == self.Role.USTOZ

    def is_dekan(self):
        return self.role == self.Role.DEKAN
