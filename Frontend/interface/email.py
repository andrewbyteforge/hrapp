from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from Backend.schools.models import School
import logging
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

class EmailSchoolView(View):
    """
    View for preparing and displaying the interface for emailing schools.

    This view handles the GET request to fetch all schools from the database and prepare predefined email messages.
    It renders a page where users can select a school and an email message to send. In case of any exceptions,
    an HttpResponseNotFound is returned.

    Methods:
    - get(request): Renders the email interface with the list of schools and predefined messages.
    """
    def get(self, request):
        try:
            schools = School.objects.all()
            school_data = [{'id': school.id, 'name': school.name, 'email': school.email} for school in schools]

            predefined_messages = [
                {'title': 'Invoice Message', 'body': 'Hi,\n\nHope all are well\n\nPlease find the attached invoice.\n\nThis is the invoice message body.\n\nBest regards,\nFake Message'},
                {'title': 'Reminder Message', 'body': 'This is a reminder.\n\nBest regards,\nFake Business'},
            ]

            return render(request, 'email_school.html', {
                'school_data': school_data,
                'predefined_messages': predefined_messages
            })
        except Exception as e:
            # Log the error with stack trace
            logger.exception("Error fetching schools in EmailSchoolView: %s", str(e))
            # error message without exposing error details
            context = {'error_message': 'An error occurred while fetching school data.'}
            # generic HTTP error response
            return render(request, 'error_page.html', context, status=500)

class SendingEmailView(View):
    """
    View for handling the sending of an email to a selected school.

    This view processes the POST request to send an email to the selected school with the provided subject,
    message, and attachment. After sending the email, it redirects to a landing page. The GET request method
    is not allowed for this view.

    Methods:
    - post(request): Processes the email sending operation and redirects to the landing page.
    - get(request): Returns HttpResponseNotAllowed as GET requests are not supported.
    """
    def post(self, request):
        school_email = request.POST.get('schoolEmail')
        subject = request.POST.get('emailSubject')
        message = request.POST.get('emailBody')
        attachment = request.FILES.get('pdfAttachment')
        try:
            email = EmailMessage(
                subject,
                message,
                '#',  # From email
                [school_email]  # To email
            )
            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)
            email.send()
            logger.info(f"Email sent successfully to {school_email}.")            
            return redirect('landingpage')
        except Exception as e:
            logger.exception("Error in SendingEmailView while sending email: %s", str(e))            
            return redirect('error_page')

    def get(self, request):
        return HttpResponseNotAllowed(['POST'])
