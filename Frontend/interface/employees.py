from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
import logging
from django.views import View
from Backend.schools.models import Employee, School
from .forms import InvoiceForm, EditEmployeeForm, AddEmployeeForm
from django.http import JsonResponse
import json
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST


import logging
logger = logging.getLogger(__name__)

class EmployeesView(View):
    """
    View for listing all employees.

    This view fetches all employees from the database and renders them on a page. It is accessed
    through a GET request, which displays the list of employees.

    Methods:
    - get(request): Renders the employees list page with all employees fetched from the database.
    """
    def get(self, request):
        try:
            employees = Employee.objects.all()
            logger.info("Fetched all employees for EmployeesView")
            return render(request, 'employees.html', {'employees': employees})
        except Exception as e:
            logger.exception("Failed to fetch employees in EmployeesView: %s", str(e))
            return HttpResponseNotFound('An error occurred')

    def post(self, request):
        try:
            employee_id = request.POST.get('employee_id')
            if not employee_id:
                return HttpResponseForbidden('Invalid employee ID')

            employee = Employee.objects.filter(id=employee_id)
            if employee.exists():
                employee.delete()
                logger.info(f"Employee {employee_id} deleted successfully")
            else:
                logger.info(f"Employee {employee_id} not found")
            
            return redirect('employees')  # Redirect back to the employees list
        except Exception as e:
            logger.exception("Failed to delete employee in EmployeesView: %s", str(e))
            return HttpResponseNotFound('An error occurred while deleting the employee')
        
        
class EditEmployeeView(UpdateView):
    model = Employee
    form_class = EditEmployeeForm
    template_name = 'edit_employee.html' 
    pk_url_kwarg = 'employee_id'
    success_url = reverse_lazy('employees')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.exception("Failed to update employee in EditEmployeeView: %s", str(e))
            form.add_error(None, 'An error occurred while updating the employee.')
            return self.form_invalid(form)       
        


class EmployeeDashboardView(View):
    """
    View for displaying an individual employee's dashboard.

    This view handles displaying detailed information about a specific employee, including their
    associated schools and other relevant data. It supports both GET and POST requests. The GET request
    displays the dashboard, while the POST request can be used to update the employee's information.

    Methods:
    - get(request, employee_id): Fetches a specific employee's details and renders the dashboard.
    - post(request, employee_id): Handles updates to the employee's details (implementation needed).
    """
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            associated_schools = employee.schools.all()
            units_range = [i * 0.5 for i in range(0, 42)]

            all_schools = School.objects.all()
            current_selections = request.session.get('current_selections', {})

            for school in associated_schools:
                selections = current_selections.get(school.id, {})
                school.current_units_worked = selections.get('units_worked', 0)
                school.current_unit_price = selections.get('unit_price', '')

            context = {
                'employee': employee,
                'schools': associated_schools,
                'units_range': units_range,
                'MONTH_CHOICES': InvoiceForm.MONTH_CHOICES,
                'all_schools': all_schools,
            }
            return render(request, 'employee_dashboard.html', context)

        except Employee.DoesNotExist:
            logger.error(f"Employee with id {employee_id} not found.")
            return HttpResponseNotFound('Employee not found')
        except Exception as e:
            logger.error(f"Error in EmployeeDashboardView: {e}", exc_info=True)
            return HttpResponseNotFound('An error occurred')

    def post(self, request, employee_id):
        
        pass

class AddSchoolToEmployeeView(View): 
    """
    View for adding a school to an employee's list of associated schools.

    This view processes a POST request to add a specified school to the list of schools associated
    with a given employee. It expects JSON data containing the school ID and updates the database
    accordingly.

    Methods:
    - post(request, employee_id): Processes the POST request to associate a school with an employee.
    """  
    def post(self, request, employee_id):
        """
        Adds a school to an employee's list of associated schools.

        On a POST request, this view processes the request to add a specified school to the
        list of schools associated with a given employee. It handles JSON data containing the
        school ID and updates the database accordingly.

        Parameters:
        - request: HttpRequest object containing metadata about the request.
        - employee_id: The ID of the employee to whom the school is to be added.

        Returns:
        - JsonResponse indicating the status of the operation.
        """
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                school_id = data.get('school_id')
                if not school_id:
                    logger.warning("School ID not provided in AddSchoolToEmployeeView for employee %s", employee_id)
                    return JsonResponse({'error': 'School ID not provided'}, status=400)

                employee = Employee.objects.get(id=employee_id)
                school = School.objects.get(id=school_id)
                employee.schools.add(school)
                
                logger.info("Added school %s to employee %s", school_id, employee_id)
                return JsonResponse({'status': 'success'})

            except json.JSONDecodeError as e:
                logger.exception("JSON Decode Error in AddSchoolToEmployeeView: %s", str(e))
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

            except Employee.DoesNotExist:
                logger.error("Employee with id %s not found in AddSchoolToEmployeeView", employee_id)
                return JsonResponse({'error': 'Employee not found'}, status=404)

            except School.DoesNotExist:
                logger.error("School with id %s not found in AddSchoolToEmployeeView", school_id)
                return JsonResponse({'error': 'School not found'}, status=404)

            except Exception as e:
                logger.exception("Error in AddSchoolToEmployeeView: %s", str(e))
                return JsonResponse({'error': 'An error occurred'}, status=500)

        else:
            logger.warning("Invalid request method in AddSchoolToEmployeeView for employee %s", employee_id)
            return JsonResponse({'error': 'Invalid request method'}, status=405)


class RemoveSchoolFromEmployeeView(View):
    """
    Removes a school from an employee's list of associated schools.

    On a POST request, this view processes the request to remove a specified school from the
    list of schools associated with a given employee, identified by the school ID in the JSON data.

    Parameters:
    - request: HttpRequest object containing metadata about the request.
    - employee_id: The ID of the employee from whom the school is to be removed.

    Returns:
    - JsonResponse indicating the status of the operation.
    """
    def post(self, request, employee_id):
        try:
            data = json.loads(request.body)
            school_id = data.get('school_id')

            employee = Employee.objects.get(id=employee_id)
            school = School.objects.get(id=school_id)
            employee.schools.remove(school) 

            logger.info(f"School with ID {school_id} removed from employee {employee_id}.")
            return JsonResponse({'status': 'success'})
        except Employee.DoesNotExist:
            logger.error(f"Employee with ID {employee_id} not found.")
            return JsonResponse({'status': 'error', 'message': 'Employee not found'}, status=404)
        except School.DoesNotExist:
            logger.error(f"School with ID {school_id} not found.")
            return JsonResponse({'status': 'error', 'message': 'School not found'}, status=404)
        except Exception as e:
            logger.exception(f"Error in removing school from employee: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)

    
class EmployeeListView(View):
    """
    View for listing all employees in a simple list format.

    This view fetches all employees from the database and displays them in a list format. It is meant
    to be a simple, straightforward representation of employee data and is accessed through a GET request.

    Methods:
    - get(request): Renders a page with a list of all employees.
    """
    def get(self, request):
        try:
            employees = Employee.objects.all()
            return render(request, 'employees.html', {'employees': employees})
        except Exception as e:
            # Log exception with stack trace 
            logger.exception("Error fetching employees in EmployeeListView: %s", str(e))
            # generic error message to the client, without exposing details
            context = {'error_message': 'An error occurred while fetching employee data.'}
            # HttpResponseServerError to indicate a server-side error
            return render(request, 'error_page.html', context, status=500)


@require_POST
def delete_employee(request):
    employee_id = request.POST.get('employee_id')
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    # Redirect to the page that lists employees
    return redirect('employees') 




class AddEmployeeView(View):
    def get(self, request):
        form = AddEmployeeForm()
        return render(request, 'add_employee.html', {'form': form})

    def post(self, request):
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')  # Redirect to the employee list page
        else:
            # Always return an HttpResponse (render the form with errors)
            return render(request, 'add_employee.html', {'form': form})