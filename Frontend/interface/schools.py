from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from Backend.schools.models import School
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import HttpResponseServerError
import traceback
import logging

logger = logging.getLogger('logging_app')

class SchoolsView(View):
    """
    View for listing all schools in a paginated format.

    This view fetches all schools from the database, orders them by name, and displays them on a page
    using pagination. It handles the GET request to display a list of schools, paginated to show a set
    number of schools per page.

    Methods:
    - get(request): Renders the schools list page with pagination.
    """
    def get(self, request):
        try:
            school_list = School.objects.order_by('name')
            total_schools = school_list.count()
            paginator = Paginator(school_list, 10)
            page_number = request.GET.get('page')
            schools = paginator.get_page(page_number)
            return render(request, 'schools.html', {'schools': schools, 'total_schools': total_schools})
        except Exception as e:
            logger.exception("Failed to fetch schools in SchoolsView: %s", e)
            return HttpResponseServerError('An error occurred while fetching school data.')

class EditSchoolView(UpdateView):
    """
    View for editing a school's details.

    This view extends Django's UpdateView to handle the editing of a school's details. It updates
    fields like name, address, postcode, and email of a specified school. The view renders a form
    pre-filled with the school's current details and saves changes upon form submission.

    Attributes:
    - model: The model being updated (School).
    - fields: List of fields in the model to be updated.
    - template_name: Template used to render the edit form.
    - pk_url_kwarg: URL keyword argument to identify the school.
    - context_object_name: Name of the context object in the template.
    - success_url: URL to redirect to after successful update.
    """
    model = School
    fields = ['name', 'address', 'postcode', 'email']
    template_name = 'edit_school.html'
    pk_url_kwarg = 'school_id'
    context_object_name = 'school'
    success_url = reverse_lazy('schools')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.exception("Failed to update school in EditSchoolView: %s", e)
            form.add_error(None, 'An error occurred while updating the school.')
            return self.form_invalid(form)
    
class DeleteSchoolView(DeleteView):
    """
    View for deleting a school.

    This view extends Django's DeleteView to handle the deletion of a school. It is used to process
    the deletion of a specified school, identified by its ID. Upon successful deletion, it redirects
    to a specified URL.

    Attributes:
    - model: The model being deleted (School).
    - pk_url_kwarg: URL keyword argument to identify the school.
    - success_url: URL to redirect to after successful deletion.
    - template_name: Optional template used for confirmation of deletion.
    """
    model = School
    pk_url_kwarg = 'school_id'
    success_url = reverse_lazy('schools')
    template_name = 'school_confirm_delete.html'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj is None:
            logger.error("School not found with ID: %s", self.kwargs.get('school_id'))
            # Handle the case where the object doesn't exist
        return obj

    def delete(self, request, *args, **kwargs):        
        try:
            print("DeleteSchoolView is being called")
            return super().delete(request, *args, **kwargs)
        except Exception as e:
                traceback_details = traceback.format_exc()
                logger.error("Exception Type: %s", type(e).__name__)
                logger.error("Exception Message: %s", str(e))
                logger.error("Traceback: %s", traceback_details)
                return HttpResponseServerError('An error occurred while deleting the school.')


