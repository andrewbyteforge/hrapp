from django.db import models


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=140, default='Unknown', blank=True, null=True)
    postcode = models.CharField(max_length=10, default='Unknown', blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)  # Add this line

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    month = models.DateField()
    attendance_percentage = models.FloatField()
    
       
class InvoiceCounter(models.Model):
    last_invoice_number = models.IntegerField(default=0)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo_url = models.URLField(blank=True, null=True) # Assuming you store image URLs
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    goals_active = models.IntegerField(default=0)
    goals_completed = models.IntegerField(default=0)
    progress = models.IntegerField(help_text="Percentage of goals completed", default=0)
    tasks_due = models.IntegerField(default=0)
    performance_score = models.IntegerField(help_text="Performance score out of 100", default=0)
    success_rate = models.IntegerField(help_text="Success rate based on projects", default=0)
    innovation_score = models.IntegerField(help_text="Score for innovation and ideas", default=0)
    schools = models.ManyToManyField(School, related_name='employees')
    # Add other fields as necessary

    def __str__(self):
        return self.name
    
class EarningsRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    month_year = models.CharField(max_length=20)  # For simplicity, could be 'January 2024', etc.
    total_earned = models.DecimalField(max_digits=10, decimal_places=2)
    employ_earned = models.DecimalField(max_digits=10, decimal_places=2)
    ed5_earned = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # For recording the exact time of entry

    def __str__(self):
        return self.employee
