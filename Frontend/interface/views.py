from django.shortcuts import render
from Backend.schools.models import School, Employee, EarningsRecord, Attendance
from django.http import HttpResponseServerError
from django.core.paginator import Paginator
from .forms import YourForm  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django import template
from django.db.models import Sum
from django.http import JsonResponse
from collections import defaultdict
from decimal import Decimal
from django.shortcuts import redirect
from datetime import datetime
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


import logging
logger = logging.getLogger('logging_app')

# the Home page
def landingpage(request):   
    return render(request, 'landingpage.html')

register = template.Library()
@register.filter(name='multiply')
def multiply(value, arg):
    """
    Custom template filter to multiply two values.

    This filter multiplies the given 'value' by the 'arg' and returns the result.
    If either 'value' or 'arg' cannot be converted to a float, it logs an error and returns 0.

    Parameters:
    - value: The first number to be multiplied.
    - arg: The second number to be multiplied.

    Returns:
    - The product of 'value' and 'arg' as a float.
    - Returns 0 if either value is not a number.
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError) as e:
        logger.error("Error in multiply filter: Unable to convert %s or %s to float. Error: %s", value, arg, e)
        return 0

@csrf_exempt
@require_POST
def calculate_earnings(request):
    """
    Calculates and returns earnings based on the provided school, units worked, and unit price.

    This view processes a POST request containing JSON data with school ID, units worked,
    and unit price. It calculates total earnings, employ earned, and Ed5 earned, and returns
    these values in a JsonResponse.

    Returns:
    - JsonResponse containing calculated earnings.
    """
    try:
        data = json.loads(request.body)
        school_id = data.get('school_id')
        units_worked = float(data.get('units_worked', 0))
        unit_price = float(data.get('unit_price', 0))    
        total_earned = units_worked * unit_price
        total_earned_formatted = "{:.2f}".format(total_earned)
        
        # Employ Earned Calculation
        employee_hourly_rate = 20.00
        hours_per_unit = 8 if unit_price == 350.00 else 4 if unit_price == 200.00 else 6 if unit_price == 185.00 else 0
        employ_earned = units_worked * hours_per_unit * employee_hourly_rate
        employ_earned_formatted = "{:.2f}".format(employ_earned)    
        
        # Ed5 Earned
        ed5_earned = total_earned - employ_earned

        return JsonResponse({
            'total_earned': total_earned_formatted,
            'employ_earned': employ_earned_formatted,
            'ed5_earned': ed5_earned,
        })
    except json.JSONDecodeError as e:
        logger.error("JSONDecodeError in calculate_earnings: %s", e)
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except (ValueError, TypeError) as e:
        logger.error("Error processing earnings data in calculate_earnings: %s", e)
        return JsonResponse({'error': 'Error in data processing'}, status=400)
    except Exception as e:
        logger.exception("Unexpected error in calculate_earnings: %s", e)
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

@csrf_exempt
@require_POST
def save_earnings(request):
    """
    Saves or updates earnings records for a given school and employee.

    On a POST request, this view processes the JSON data containing school ID, employee ID,
    units worked, unit price, and month/year. It calculates the earnings and updates or creates
    the EarningsRecord in the database.

    Returns:
    - JsonResponse indicating the success or failure of the operation.
    """
    data = json.loads(request.body)
    school_id = data.get('school_id')
    employee_id = data.get('employee_id')  # Ensure this is being passed correctly
    units_worked = float(data.get('units_worked', 0))
    unit_price = float(data.get('unit_price', 0))
    month_year = data.get('month_year', '')
    try:
        employee = Employee.objects.get(id=employee_id)
        school = School.objects.get(id=school_id)
        # Calculate employ_earned and ed5_earned
        employee_hourly_rate = 20.00
        hours_per_unit = 8 if unit_price == 350.00 else 4 if unit_price == 200.00 else 6 if unit_price == 185.00 else 0
        employ_earned = units_worked * hours_per_unit * employee_hourly_rate
        total_earned = units_worked * unit_price
        ed5_earned = total_earned - employ_earned
        # Update or create the record
        EarningsRecord.objects.update_or_create(
            employee=employee,
            school=school,
            month_year=month_year,
            defaults={
                'total_earned': total_earned,
                'employ_earned': employ_earned,
                'ed5_earned': ed5_earned
            }
        )
        return JsonResponse({'status': 'success'})

    except Employee.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Employee not found'}, status=404)
    except School.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'School not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def analytics_data(request):
    """
    Provides analytics data for selected employees.

    This view fetches earnings records for a selected employee and calculates monthly earnings,
    Ed5 earnings, and employ earnings. It returns this data in a context rendered to a template
    for analytics visualization.

    Returns:
    - HttpResponse object with the rendered analytics data.
    """
    try:
        employees = Employee.objects.all()
        selected_employee_id = request.GET.get('employee_id')
        earnings_data = defaultdict(Decimal)
        ed5_earnings_data = defaultdict(Decimal)
        employ_earnings_data = defaultdict(Decimal)  # For employ earned    
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]

        if selected_employee_id:
            records = EarningsRecord.objects.filter(employee_id=selected_employee_id)
            for record in records:
                month = record.month_year.split()[0] if record.month_year else None
                if month in months:
                    earnings_data[month] += record.total_earned
                    ed5_earnings_data[month] += record.ed5_earned
                    employ_earnings_data[month] += record.employ_earned

            monthly_earnings = [float(earnings_data.get(month, 0)) for month in months]
            monthly_ed5_earnings = [float(ed5_earnings_data.get(month, 0)) for month in months]
            monthly_employ_earnings = [float(employ_earnings_data.get(month, 0)) for month in months]
            total_ed5_earned = sum(monthly_ed5_earnings)
            total_employ_earned = sum(monthly_employ_earnings)
            total_earnings = sum(monthly_earnings)
        else:
            monthly_earnings = monthly_ed5_earnings = monthly_employ_earnings = [0] * len(months)
            total_ed5_earned = total_employ_earned = total_earnings = 0

        context = {
            'employees': employees,
            'selected_employee_id': int(selected_employee_id) if selected_employee_id else None,
            'months': months,
            'monthly_earnings': monthly_earnings,
            'monthly_ed5_earnings': monthly_ed5_earnings,
            'monthly_employ_earnings': monthly_employ_earnings,
            'total_ed5_earned': total_ed5_earned,
            'total_employ_earned': total_employ_earned,
            'total_earnings': total_earnings,
        }
        return render(request, 'analytics_data.html', context)

    except Exception as e:
        logger.exception("Error in analytics_data view: %s", e)
        # Optionally, you can provide a user-friendly message or redirect to an error page
        return HttpResponseServerError('An error occurred while fetching analytics data.')

def stats(request):
    """
    Renders a page with statistics for all schools.

    This view fetches all schools and their related data to display statistics like total earnings
    and others. It passes this information in the context to the rendered template.

    Returns:
    - HttpResponse object with the rendered statistics page.
    """
    try:        
        schools = School.objects.all()
        context = {'schools': schools}
        return render(request, 'stats.html', context)
    except Exception as e:
        logger.error("Error in stats view: %s", e)
        return HttpResponseServerError('An error occurred while fetching stats.')

def fetch_school_data(request):
    """
    Fetches and returns financial data for a specific school.

    This view, on receiving a school ID via GET request, fetches earnings data for that school.
    It processes and summarizes the earnings per month and returns this data in a JsonResponse.

    Parameters:
    - request: HttpRequest object containing the school ID.

    Returns:
    - JsonResponse with earnings data for the specified school.
    - JsonResponse with error message if school is not found or if no school ID is provided.
    """
    try:
        school_id = request.GET.get('schoolId')
        if not school_id:
            logger.error("No school ID provided in fetch_school_data request.")
            return JsonResponse({'error': 'No school ID provided'}, status=400)
    
        school = School.objects.get(id=school_id)        
        earnings_per_month = EarningsRecord.objects.filter(school=school).values('month_year').annotate(total_earnings=Sum('total_earned')).order_by('month_year')

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        earnings_map = {month: 0 for month in months}  # Initialize map with zero values

        for e in earnings_per_month:
            month_year_split = e['month_year'].split()
            if month_year_split and month_year_split[0] in months:
                earnings_map[month_year_split[0]] = e['total_earnings']

        monthly_data = [earnings_map[month] for month in months]
        total_year_earnings = sum(monthly_data)
        total_ed5_earned = EarningsRecord.objects.filter(school=school).aggregate(total_ed5=Sum('ed5_earned'))['total_ed5'] or 0

        data = {
            'labels': months,
            'datasets': [{
                'label': 'Total Earnings',
                'data': monthly_data,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.1
            }],
            'total_year_earnings': total_year_earnings,            
            'total_ed5_earned': total_ed5_earned,
        }
        return JsonResponse(data)
    except School.DoesNotExist:
        logger.error(f"School with ID {school_id} not found in fetch_school_data.")
        return JsonResponse({'error': 'School not found'}, status=404)
    except Exception as e:
        logger.exception(f"Unexpected error in fetch_school_data: {e}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    

    
def delete_all_schools(request):
    # Delete all school entries from the database
    School.objects.all().delete()
    # Redirect back to the page where the button was clicked
    return redirect('schools') 




def client_analytics(request):
    
    return render(request, 'client_analytics.html')


def employee_analytics(request):
    
    return render(request, 'employee_analytics.html')

def data(request):
    
    return render(request, 'data.html')



def client_attendance(request):
    current_year = datetime.now().year
    years = range(2017, current_year + 1)
    schools = School.objects.all()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render(request, 'client_attendance.html', {'schools': schools, 'years': years, 'months': months})





def attendance_data(request):
    school_id = request.GET.get('school_id')
    year = request.GET.get('year')
    data = Attendance.objects.filter(
        school_id=school_id, 
        month__year=year
    ).annotate(
        month_label=ExtractMonth('month')  # Extract the month number
    ).values(
        'month_label', 'attendance_percentage'
    )
    return JsonResponse(list(data), safe=False)




def add_attendance(request):
    current_year = datetime.now().year
    schools = School.objects.all()
    years = range(2017, current_year + 1)  # Creates a range from 2017 to the current year
    return render(request, 'add_attendance.html', {'schools': schools, 'years': years})







from datetime import datetime
from django.http import HttpResponse

@csrf_exempt
def submit_attendance(request):
    if request.method == 'POST':
        school_id = request.POST.get('school')
        year = request.POST.get('year')
        month_value = request.POST.get('month')
        attendance_percentage = float(request.POST.get('attendance_percentage'))

        # Construct a valid date string (YYYY-MM-DD format)
        date_str = f"{year}-{month_value}-01"

        try:
            school = get_object_or_404(School, id=school_id)
            month = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Try to get an existing attendance record
            attendance_record, created = Attendance.objects.get_or_create(
                school=school,
                month=month,
                defaults={'attendance_percentage': attendance_percentage}
            )

            if not created:
                # Update the existing record with the new attendance percentage
                attendance_record.attendance_percentage = attendance_percentage
                attendance_record.save()

            return redirect('client_attendance')
        
        except (ValueError, TypeError):
            return HttpResponse("Invalid attendance percentage format", status=400)
    return redirect('add_attendance')



def delete_database(request):
    # Delete all records from the AttendanceData model
    Attendance.objects.all().delete()
    return redirect('data')  # Redirect to a suitable URL after deletion


from django.db.models.functions import ExtractMonth

def get_data_for_year(year):
    # Query the Attendance model for the specified year
    attendance_data = Attendance.objects.filter(
        month__year=year
    ).annotate(
        month_label=ExtractMonth('month')  # Extract the month number
    ).order_by('month_label').values(
        'month_label', 'attendance_percentage'
    )

    # Initialize a list with 12 zeros for each month
    monthly_data = [0] * 12

    for attendance in attendance_data:
        # Use the 'month_label' from each attendance record
        month_index = attendance['month_label'] - 1  # Adjust for list indexing
        monthly_data[month_index] = attendance['attendance_percentage']

    return monthly_data



def comparison_year(request):
    year = request.GET.get('year')
    print(f"Received year: {year}")  # Logging the received year

    if year:
        data_for_year = get_data_for_year(year)
        print(f"Data for year {year}: {data_for_year}")  # Logging the data

        formatted_data = {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            'values': data_for_year
        }

        return JsonResponse({'data': formatted_data})
    else:
        return JsonResponse({'error': 'No year provided'}, status=400)







