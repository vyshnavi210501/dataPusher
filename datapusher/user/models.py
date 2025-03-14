from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, created_by=None, updated_by=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            created_by=created_by,
            updated_by=updated_by,  # Ensure updated_by is set
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Role(models.Model):
    class RoleTypes(models.TextChoices):
        ADMIN = "Admin", "Admin"
        NORMAL_USER = "Normal User", "Normal User"
    role_name=models.CharField(choices=RoleTypes.choices,unique=True,max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name