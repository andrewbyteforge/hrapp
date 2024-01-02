from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from . import invoice, email, employees, schools





urlpatterns = [
    
    # Home Page
    path('', views.landingpage, name='landingpage'),

    # INVIOCE
    path('finance/', invoice.FinanceView.as_view(), name='finance'),
    path('regular_Invoice/', invoice.RegularInvoiceView.as_view(), name='regular_Invoice'),
    path('custom_invoice/', invoice.CustomInvoiceView.as_view(), name='custom_invoice'),
    path('custom_invoice_preview/', invoice.CustomInvoicePreviewView.as_view(), name='custom_invoice_preview'),
    path('test/', invoice.TestView.as_view(), name='test'),
    

    # SCHOOLS
    path('schools/', schools.SchoolsView.as_view(), name='schools'),
    path('edit_school/<int:school_id>/', schools.EditSchoolView.as_view(), name='edit_school'),
    path('delete_school/<int:school_id>/', schools.DeleteSchoolView.as_view(), name='delete_school'),

    path('employee/<int:employee_id>/add-school/',
         employees.AddSchoolToEmployeeView.as_view(), name='add_school_to_employee'),
    path('delete-all-schools/', views.delete_all_schools, name='delete_all_schools'),
    
    # EMAIL
    path('email_school/', email.EmailSchoolView.as_view(), name='email_school'),
    path('send_email/', email.SendingEmailView.as_view(), name='sending_email'),

    # EMPLOYEES
    path('edit_employee/<int:employee_id>/', employees.EditEmployeeView.as_view(), name='edit_employee'),
    path('delete_employee/', employees.delete_employee, name='delete_employee'),
    path('add_employee/', employees.AddEmployeeView.as_view(), name='add_employee'),
    path('employee_dashboard/<int:employee_id>/',
         employees.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('employees/', employees.EmployeesView.as_view(), name='employees'),
    path('employee/<int:employee_id>/remove-school/',
         employees.RemoveSchoolFromEmployeeView.as_view(), name='remove_school_from_employee'),
     path('employee_list/', employees.EmployeeListView.as_view(), name='employee_list'),
     
     
    # CALCULATIONS
    path('calculate-earnings/', views.calculate_earnings,
         name='calculate_earnings'),
    path('save-earnings/', views.save_earnings, name='save_earnings'),

    # ANALYTICS FOR SCHOOLS
    path('analytics_data/', views.analytics_data, name='analytics_data'),
    path('stats/', views.stats, name='stats'),
    path('fetch_school_data/', views.fetch_school_data, name='fetch_school_data'),
]


# Serve static and media files from development server
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
