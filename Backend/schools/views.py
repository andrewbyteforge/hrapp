from django.shortcuts import render, redirect
from .models import School
from .models import InvoiceCounter
from Frontend.interface.forms import SchoolForm
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from Frontend.interface.forms import SchoolForm
from Backend.schools.models import InvoiceCounter
from django.views import View

import logging
logger = logging.getLogger('logging_app')

class InvoiceNumberView(View):
    """
    View for generating and displaying a new sequentially incremented invoice number.

    This view handles the GET request to generate a new invoice number. It retrieves the last used
    invoice number from the InvoiceCounter model, increments it by one, and saves it back to the model.
    The new invoice number is then displayed on the 'test.html' page. If an error occurs, the user
    is redirected to an 'error_page.html' with an error message.

    Methods:
    - get(request): Renders a page displaying the new invoice number or an error message.
    """
    def get(self, request):
        try:
            # Retrieve or create the last invoice number
            counter, created = InvoiceCounter.objects.get_or_create(id=1)
            new_invoice_number = counter.last_invoice_number + 1
            # Update the counter
            counter.last_invoice_number = new_invoice_number
            counter.save()
            # Format the invoice number
            formatted_invoice_number = str(new_invoice_number).zfill(3)  # Pad with zeros
        except Exception as e:
            # Log the error
            logger.error("Error creating invoice number: %s", str(e), exc_info=True)
            context = {'error_message': 'An error occurred while generating the invoice number.'}
            return render(request, 'error_page.html', context)

        # Proceed as normal if no exceptions
        return render(request, 'test.html', {'invoiceNumber': formatted_invoice_number})

class AddSchoolsView(View):
    """
    View for handling the addition of new schools through a form submission.

    This view renders a form for adding new schools and processes the form submission.
    On a POST request, if the form is valid, it attempts to save the new school data
    to the database and redirects to the 'schools' page. In case of any exceptions
    during the save operation or form validation errors, appropriate feedback is provided
    to the user.

    Methods:
    - get(request): Renders a form for adding schools.
    - post(request): Processes the form submission for adding a new school.
    """
    
    def get(self, request):
        form = SchoolForm()
        return render(request, 'add_schools.html', {'form': form})

    def post(self, request):
        form = SchoolForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                logger.info("New school added: %s", form.cleaned_data['name'])
                return redirect('schools')
            except Exception as e:
                logger.error("Error saving school: %s", str(e), exc_info=True)
                messages.error(request, 'An unexpected error occurred while saving the school.')
        return render(request, 'add_schools.html', {'form': form})



