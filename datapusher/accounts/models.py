from django.db import models
from django.contrib.auth import get_user_model
from user.models import Role
import uuid
import secrets

User=get_user_model()

# Create your models here.
class Account(models.Model):
    account_id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True)
    account_name=models.CharField(max_length=50)
    app_secret_token=models.CharField(unique=True,max_length=100,default=secrets.token_hex(32))
    website=models.URLField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.CharField(max_length=100)
    updated_by=models.CharField(max_length=100)

class Destination(models.Model):
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    url=models.URLField(max_length=200)
    http_method = models.CharField(
        max_length=10, 
        choices=[
            ("GET", "GET"), 
            ("POST", "POST"), 
            ("PUT", "PUT"),
            ("DELETE", "DELETE"), 
            ("PATCH", "PATCH")
        ]
    )
    headers = models.JSONField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.CharField(max_length=100)
    updated_by=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.account} {self.url} {self.http_method}"
    
class AccountMember(models.Model):
    account_id=models.ForeignKey(Account,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    role_id=models.ForeignKey(Role,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.CharField(max_length=100)
    updated_by=models.CharField(max_length=100)

class Log(models.Model):
    event_id=models.UUIDField(unique=True)
    account_id=models.ForeignKey(Account,on_delete=models.CASCADE)
    received_timestamp = models.DateTimeField()
    processed_timestamp = models.DateTimeField(null=True,blank=True)
    received_data = models.JSONField()
    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)