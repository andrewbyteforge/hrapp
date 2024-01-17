from django import forms
from Backend.schools.models import School
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from Backend.schools.models import Employee

class InvoiceForm(forms.Form):
    # Dropdown for selecting a school from all available schools in the database.
    select_school = forms.ModelChoiceField(queryset=School.objects.all(), label='Select School', required=False)

    # Decimal field for inputting the number of units worked, with a step of 0.5.
    units_worked = forms.DecimalField(min_value=0.5, max_value=30, decimal_places=1, required=False, widget=forms.NumberInput(attrs={'step': '0.5'}))

    # Date fields for the date of invoice and due date, using a date picker widget.
    date_of_invoice = forms.DateField(widget=forms.TextInput(attrs={'class': 'datetimepicker'}), required=False, input_formats=['%d/%m/%Y'])
    due_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datetimepicker'}), required=False, input_formats=['%d/%m/%Y'])

    # Choice field for selecting a description of the work done.
    work_description = forms.ChoiceField(choices=[(0, ''), ('Half day of  support.', 'Half day of  support.'), ('Full day of support. ', 'Full day of support. '), ('Full day of admin support.  ', 'Full day of admin support.  '), ('other', 'other')], required=False)

    # Choice field for selecting the unit price.
    unit_price = forms.ChoiceField(choices=[('', ''), ('185.00', '185.00'), ('200.00', '200.00'), ('350.00', '350.00')])

    # Choices for months in 2024, to be used in a dropdown.
    MONTH_CHOICES = [
        ('', ''), ('January 2024', 'January 2024'), ('February 2024', 'February 2024'), ('March 2024', 'March 2024'),
        ('April 2024', 'April 2024'), ('May 2024', 'May 2024'), ('June 2024', 'June 2024'),
        ('July 2024', 'July 2024'), ('August 2024', 'August 2024'), ('September 2024', 'September 2024'),
        ('October 2024', 'October 2024'), ('November 2024', 'November 2024'), ('December 2024', 'December 2024')
    ]
    month_work_took_place = forms.ChoiceField(choices=MONTH_CHOICES, required=False)

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'postcode']  # Fields to include in the form.

# Email form
class YourForm(forms.Form):
    # Email field for manually inputting an email address.
    schoolEmail = forms.EmailField(label='Email to', required=False)

    # Text fields for the subject and body of the email.
    emailSubject = forms.CharField(label='Email Subject', max_length=100)
    emailBody = forms.CharField(label='Message Body', widget=forms.Textarea)

    # File field for attaching a PDF, with validations for file type and size.
    pdfAttachment = forms.FileField(label='Attach PDF', required=False)

    def clean_pdfAttachment(self):
        # Validate the attached PDF file.
        file = self.cleaned_data.get('pdfAttachment', False)
        if file:
            if file.content_type != 'application/pdf':
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.size > 2621440:  # 2.5MB limit
                raise forms.ValidationError("The file is too large. Size should not exceed 2.5 MB.")
        return file




class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'photo_url', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            # Add any other field-specific widget you need
        }
        


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'photo_url', 'email', 'phone_number']  # Adjust the fields as per your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            # Add other widgets as needed
        }
        
        
class SchoolSelectionForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all())
