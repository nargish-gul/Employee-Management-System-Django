"""
URL configuration for ems_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from employees import views

urlpatterns = [



    

    path('admin/', admin.site.urls),
    path('employees/',include('employees.urls')),




     # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Dashboard + Employees
    path('dashboard/', views.dashboard, name='dashboard'),
    
   
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),

# User Profile
    path('profile/', views.profile, name='profile'),



# Department Management
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/edit/<int:pk>/', views.department_edit, name='department_edit'),
    path('departments/delete/<int:pk>/', views.department_delete, name='department_delete'),
    
    


# Payroll Management
    # Payroll Management
path('payroll/', views.payroll_list, name='payroll_list'),
path('payroll/add/', views.payroll_add, name='payroll_add'),
path('payroll/edit/<int:pk>/', views.payroll_edit, name='payroll_edit'),
path('payroll/delete/<int:pk>/', views.payroll_delete, name='payroll_delete'),

    





]




