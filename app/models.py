from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import pytz
from datetime import timedelta
from django.conf import settings
from cryptography.fernet import Fernet

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuários devem ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuários devem ter is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Adicione o argumento related_name aos campos groups e user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Servidor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    porta = models.PositiveIntegerField()
    porta_ssh = models.PositiveIntegerField()
    status = models.BooleanField()
    cpu = models.TextField(null=True)
    memory = models.TextField(null=True)
    disk = models.TextField(null=True)
    status_ping = models.BooleanField(default=False)
    service = models.CharField(max_length=100, null=True)
    datahora = models.DateTimeField(default=timezone.now)
    datahoradetalhes = models.DateTimeField(default=None, null=True)

    def save(self, *args, **kwargs):
        self.datahora = timezone.now().astimezone(pytz.timezone('America/Sao_Paulo'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome + ' - ' + self.service


class AcessoServidores(models.Model):
    id = models.AutoField(primary_key=True)
    apelido = models.CharField(max_length=100)
    servidor = models.CharField(max_length=100)
    bases = models.CharField(max_length=255)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    engine = models.CharField(max_length=100)
    inslots = models.BooleanField(default=False)
    is_password_encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.apelido
    
    def encrypt_password(self, password):
        ENCRYPTION_KEY = str.encode(settings.ENCRYPTION_KEY)
        cipher_suite = Fernet(ENCRYPTION_KEY)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password.decode()

    def decrypt_password(self):
        ENCRYPTION_KEY = str.encode(settings.ENCRYPTION_KEY)
        cipher_suite = Fernet(ENCRYPTION_KEY)
        decrypted_password = cipher_suite.decrypt(self.senha.encode())
        return decrypted_password.decode()
    
    def save(self, *args, **kwargs):
        if not self.is_password_encrypted:
            self.senha = self.encrypt_password(self.senha)
            self.is_password_encrypted = True
        super().save(*args, **kwargs)
    

class Expurgo(models.Model):
    id = models.AutoField(primary_key=True)
    servidor = models.ForeignKey(AcessoServidores, on_delete=models.CASCADE)
    base = models.CharField(max_length=100)
    tabela = models.CharField(max_length=100)
    tamanhomb = models.FloatField()
    deletado = models.BooleanField()
    datahora = models.DateTimeField(default=timezone.now)
    datahoratodelete = models.DateTimeField(default=None, null=True)
    datahoradeleted = models.DateTimeField(default=None, null=True)
    
    def save(self, *args, **kwargs):
        self.datahora = timezone.now().astimezone(pytz.timezone('America/Sao_Paulo'))
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('servidor', 'base', 'tabela')

    def __str__(self):
        return self.servidor + ' - ' + self.tabela

class Slots(models.Model):
    id = models.AutoField(primary_key=True)
    servidor = models.ForeignKey(AcessoServidores, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tamanho = models.CharField(max_length=100)
    status = models.BooleanField()
    datahora = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('servidor', 'nome')

    def __str__(self):
        return self.nome


