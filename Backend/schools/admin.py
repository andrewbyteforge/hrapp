from django.contrib import admin
from .models import Employee, School, InvoiceCounter, EarningsRecord

# Create access to each model via the admin panel
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    filter_horizontal = ('schools',)  
admin.site.register(School)
admin.site.register(InvoiceCounter)
admin.site.register(EarningsRecord)







