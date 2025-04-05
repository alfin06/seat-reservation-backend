from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=7, choices=[('ADMIN', 'Admin'), ('STUDENT', 'Student')], default='STUDENT')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class Seat(models.Model):
    AVAILABILITY_CHOICES = (
        (0, 'Reserved'),
        (1, 'Available'),
    )
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    is_available = models.SmallIntegerField(choices=AVAILABILITY_CHOICES, default=1)        
    # created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Seat {self.number} - {'Available' if self.is_available else 'Reserved'}"

class ClassRoom(models.Model):
    AVAILABILITY_CHOICES = (
        (0, 'Reserved'),
        (1, 'Available'),
    )
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    is_available = models.SmallIntegerField(choices=AVAILABILITY_CHOICES, default=1)  

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')