from django import forms
from .models import Employee
from .models import Department
from .models import Payroll



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'




class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']





class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'basic_salary', 'allowances', 'deductions']

