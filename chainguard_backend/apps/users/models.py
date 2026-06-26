from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        #force role for superuser
        extra_fields["role"] = "SUPERVISOR"

        #safety checks
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_supervisor=True")
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        PENDING = "PENDING", "Pending"
        OFFICER = "OFFICER", "Officer"
        STORAGE_CLERK = "STORAGE_CLERK", "Storage Clerk"
        ANALYST = "ANALYST", "Analyst"
        SUPERVISOR = "SUPERVISOR", "Supervisor"

    ROLES_REQUIRING_BADGE = {Role.OFFICER, Role.STORAGE_CLERK, Role.ANALYST}

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, error_messages={"unique": "Email already registered."})
    #default is "user with this email already exists."
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    badge_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    badge_number = models.PositiveIntegerField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PENDING)
    profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()
    
    """supervisor don't need to upload profile"""
    def save(self,*args, **kwargs):
        if self.is_superuser:
            self.profile_complete = True
        super().save(*args, **kwargs)

    class Meta:
        db_table = "users"

    


