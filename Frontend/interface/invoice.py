from django.views import View
from django.shortcuts import render
from .forms import InvoiceForm
from Backend.schools.models import School, InvoiceCounter
from django.http import HttpResponseNotAllowed
from django.views import View
from django.http import HttpResponseServerError
import logging

logger = logging.getLogger('logging_app')

class FinanceView(View):
    """
    View for handling invoice creation and processing.

    This view manages both GET and POST requests. On a GET request, it presents a blank form for invoice creation.
    On a POST request, it processes the submitted invoice form, generates an invoice number, and renders a preview
    of the invoice using the provided data. If the form is invalid, it re-renders the form for correction.

    Methods:
    - get(request): Renders a blank form for invoice creation.
    - post(request): Processes the submitted invoice form and renders the invoice preview.
    """
    def get(self, request):
        form = InvoiceForm()
        return render(request, 'finance.html', {'form': form})

    def post(self, request):
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                form_data = form.cleaned_data

                selected_school = School.objects.get(id=form_data['select_school'].id)

                counter, created = InvoiceCounter.objects.get_or_create(id=1)
                new_invoice_number = counter.last_invoice_number + 1
                counter.last_invoice_number = new_invoice_number
                counter.save()
                invoice_number = str(new_invoice_number).zfill(3)

                return render(request, 'test.html', {
                    'form_data': form_data,
                    'selected_school': selected_school,
                    'invoiceNumber': invoice_number,
                    'date_of_invoice': form_data['date_of_invoice'],
                    'due_date': form_data['due_date']
                })
            except Exception as e:
                logger.exception("Error processing invoice in FinanceView: %s", e)
                form.add_error(None, 'An error occurred while processing the invoice.')
                return render(request, 'finance.html', {'form': form})
        else:
            return render(request, 'finance.html', {'form': form})

class RegularInvoiceView(View):
    """
    View for displaying a regular invoice template.

    This view handles the GET request to render a template used for generating regular invoices.
    It is a straightforward view that simply renders the 'regular_Invoice.html' template.

    Methods:
    - get(request): Renders the 'regular_Invoice.html' template.
    """
    def get(self, request):
        # Handle GET request: Render the regular_Invoice.html template
        return render(request, 'regular_Invoice.html')

class TestView(View):
    """
    View for finalizing and displaying an invoice.

    This view handles the POST request to finalize the details of an invoice. It extracts the form data from the
    POST request, retrieves the selected school's details, generates an invoice number, and passes this data to the
    template for display. The GET request is not allowed for this view.

    Methods:
    - post(request): Finalizes the invoice and renders the preview.
    - get(request): Returns HttpResponseNotAllowed as GET requests are not supported.
    """
    def post(self, request):
        # Extract form data from POST request
        form_data = request.POST

        # Retrieve the selected school's details
        selected_school_id = form_data.get('select_school')
        selected_school = School.objects.get(id=selected_school_id)

        # Generate invoice number
        counter, created = InvoiceCounter.objects.get_or_create(id=1)
        new_invoice_number = counter.last_invoice_number + 1
        counter.last_invoice_number = new_invoice_number
        counter.save()
        invoice_number = str(new_invoice_number).zfill(3)

        # Pass the data to the template
        return render(request, 'test.html', {
            'form_data': form_data,
            'selected_school': selected_school,
            'invoiceNumber': invoice_number,
        })

    def get(self, request):
        return HttpResponseNotAllowed(['POST'])
      
class CustomInvoiceView(View):
    """
    View for rendering a page for custom invoice data entry.

    This view handles GET requests to present a form where users can enter custom invoice data. It is a simple view
    that renders a static page ('custom_invoice.html') for custom invoice data entry.

    Methods:
    - get(request): Renders the 'custom_invoice.html' page.
    """
    def get(self, request):
        # Render the page for entering custom invoice data
        return render(request, 'custom_invoice.html')
    
class CustomInvoicePreviewView(View):
    """
    View for displaying a preview of a custom invoice.

    This view manages POST requests to render a preview of the custom invoice using data entered by the user.
    The GET request is not allowed for this view, and it will return an HttpResponseNotAllowed response.

    Methods:
    - post(request): Renders a preview of the custom invoice using user-entered data.
    - get(request): Returns HttpResponseNotAllowed as GET requests are not supported.
    """
    def post(self, request):
        try:
            # Display a preview of the custom invoice
            form_data = request.POST
            return render(request, 'custom_invoice_preview.html', {'form_data': form_data})
        except Exception as e:
            logger.error("Error in CustomInvoicePreviewView (POST): %s", e)
            return HttpResponseServerError('An error occurred while rendering the custom invoice preview.')

    def get(self, request):
        try:
            return HttpResponseNotAllowed(['POST'])
        except Exception as e:
            logger.error("Error in CustomInvoicePreviewView (GET): %s", e)
            return HttpResponseServerError('An error occurred while handling the GET request.')
    
    
    
