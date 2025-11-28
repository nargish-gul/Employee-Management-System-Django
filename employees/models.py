from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


    

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    ))

    def __str__(self):
        return f"{self.employee} - {self.date}"
    



# User Profile for role management

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('hr', 'HR'),
    ('employee', 'Employee')
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    # User profile picture
profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)


def __str__(self):
        return self.user.username



# Payroll Model
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.net_salary = self.basic_salary + self.allowances - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} - {self.net_salary}"




#payslip Model
class Payslip(models.Model):
    payroll = models.ForeignKey('Payroll', on_delete=models.CASCADE)
    generated_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payslip - {self.payroll.employee} ({self.generated_on})"
