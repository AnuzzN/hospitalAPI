from django.db import models
from django.contrib.auth.models import User,AbstractUser, Group, Permission

class User(AbstractUser):
    # Add your custom fields here

    groups = models.ManyToManyField(
        Group,
        related_name='hospital_api_user_set',  # Change this related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='hospital_api_user_set',  # Change this related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )



class Department(models.Model):
    name = models.CharField(max_length=255)
    diagnostics = models.TextField()
    location = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    misc = models.TextField()

    def __str__(self):
        return f"Record {self.record_id} for {self.patient.user.username}"
