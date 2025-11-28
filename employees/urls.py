from django.urls import path
from . import views




urlpatterns = [


# API endpoint




#employee management
    path('', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),
    path('update/<int:id>/', views.employee_update, name='employee_update'),
    path('delete/<int:id>/', views.employee_delete, name='employee_delete'),




    #department management
    path('department/', views.department_list, name='department_list'),
    path('department/add/', views.department_add, name='department_add'),
    path('department/edit/<int:pk>/', views.department_edit, name='department_edit'),
    path('department/delete/<int:pk>/', views.department_delete, name='department_delete'),




    # payroll management
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/add/', views.payroll_add, name='payroll_add'),
    path('payroll/edit/<int:pk>/', views.payroll_edit, name='payroll_edit'),
    path('payroll/delete/<int:pk>/', views.payroll_delete, name='payroll_delete'),



]

