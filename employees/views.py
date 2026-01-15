

# Create your views here.
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404

from employees.permissions import hr_or_admin
from .forms import EmployeeForm
from .models import Employee, Department, Attendance
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .models import Department
from .forms import DepartmentForm


from .forms import PayrollForm
from .models import Payroll


from django.http import HttpResponse
from django.template.loader import render_to_string

from django.http import JsonResponse, HttpResponse

from datetime import date
import calendar


from .models import *

# Employee CRUD Views

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

    
@login_required
@hr_or_admin
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

@login_required
def employee_update(request, id):
    emp = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    form = EmployeeForm(instance=emp)
    return render(request, 'employee_form.html', {'form': form})


@login_required
def employee_delete(request, id):
    emp = get_object_or_404(Employee, id=id)
    emp.delete()
    return redirect('employee_list')






# Dashboard view
from django.db.models import Count
from datetime import date

@login_required
def dashboard(request):
    today = date.today()
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()

    # ===== TODAY ATTENDANCE =====
    present_today = Attendance.objects.filter(
        date=today, status="Present"
    ).count()

    leave_today = Attendance.objects.filter(
        date=today, status="Leave"
    ).count()

    absent_today = total_employees - (present_today + leave_today)

    #  Employees per department
    dept_data = Department.objects.annotate(emp_count=Count('employee'))
    dept_names = [d.name for d in dept_data]
    dept_counts = [d.emp_count for d in dept_data]

    #  Attendance status
    attendance_data = Attendance.objects.filter(date=date.today()) \
        .values('status').annotate(count=Count('id'))

    attendance_labels = [a['status'] for a in attendance_data]
    attendance_counts = [a['count'] for a in attendance_data]


    # monthly attendence
    year = today.year
    month = today.month
    days_in_month = calendar.monthrange(year, month)[1]

    days = list(range(1, days_in_month + 1))
    present_counts = []
    leave_counts = []
    absent_counts = []

    for day in days:
        present = Attendance.objects.filter(
            date=date(year, month, day),
            status="Present"
        ).count()

        leave = Attendance.objects.filter(
            date=date(year, month, day),
            status="Leave"
        ).count()

        absent = total_employees - (present + leave)

        present_counts.append(present)
        leave_counts.append(leave)
        absent_counts.append(absent)


    return render(request, 'dashboard.html', {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'present_today': present_today,
        'leave_today': leave_today,
        'absent_today': absent_today,

        'dept_names': dept_names,
        'dept_counts': dept_counts,


        'attendance_labels': attendance_labels,
        'attendance_counts': attendance_counts,

        'days': days,
        'present_counts': present_counts,
        'leave_counts': leave_counts,
        'absent_counts': absent_counts,  
    })



# Authentication Views
#template login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')






# Attendance Views

@login_required
def attendance_list(request):
    today = request.GET.get("date", str(date.today()))
    records = Attendance.objects.filter(date=today)

    return render(request, 'attendance/attendance_list.html', {
        "records": records,
        "selected_date": today
    })


@login_required
def attendance_mark(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        for emp in employees:
            status = request.POST.get(str(emp.id))
            if status:
                Attendance.objects.update_or_create(
                    employee=emp,
                    date=date.today(),
                    defaults={'status': status}
                )
        return redirect('attendance_list')

    return render(request, 'attendance/attendance_mark.html', {"employees": employees})


# Registration View with Role Assignment
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)
        profile = user.userprofile
        profile.role = role
        profile.save()

        return redirect('login')

    return render(request, 'authentication/register.html')


# User Profile View
@login_required
def profile(request):
    emp = Employee.objects.filter(email=request.user.email).first()

    if not emp:
        return render(request, 'profile/no_profile.html')

    attendance_count = Attendance.objects.filter(employee=emp).count()
    present_count = Attendance.objects.filter(employee=emp, status="Present").count()

    return render(request, 'profile/profile.html', {
        "emp": emp,
        "attendance_count": attendance_count,
        "present_count": present_count
    })





# department views



@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department/department_list.html', {'departments': departments})


@login_required
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department/department_form.html', {'form': form})


@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department/department_form.html', {'form': form})


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('department_list')




# payroll views
@login_required
def payroll_list(request):
    payrolls = Payroll.objects.all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})


@login_required
def payroll_add(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'payroll/payroll_form.html', {'form': form})


@login_required
def payroll_edit(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm(instance=payroll)
    return render(request, 'payroll/payroll_form.html', {'form': form})


@login_required
def payroll_delete(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    payroll.delete()
    return redirect('payroll_list')




# salary details 
@login_required
def salary_details(request, emp_id):
    salary = salary.objects.get(employee_id=emp_id)

    total_salary = salary.basic_salary + salary.allowances

    context = {
        'salary': salary,
        'total_salary': total_salary,
    }
    return render(request, 'salary_details.html', context)










