<b>What is this ? </b>
<br>
<br>
This is an HR application to part automate the issuing of invoices, viewing statistics and employee earnings.

To understand this further let’s create in our minds a business named Ed5. Ed5 is a business that works in this case with schools carrying out work on their behalf. The schools can be replaced with any client.
<br>
<br>
<b>Finance: </b>
<br>
The finance section comprises of two options. Regular Invoice and Custom Invoice. Regular Invoice provides preset values where custom Invoice allows for free text. Both invoices are then saved on the desktop or a folder of your choice before being emailed to the client.
The school value in Finance is populated from the database of schools that are added by the user.
<br>
<br>
<b>Employees: </b>
<br>
This section allows the creation of employees along with the editing of certain details. Within the view dashboard of the employee schools (clients) can be assigned and calculations made regarding company earning / employee earnings.
Of course, the school (client) can also be deleted.
<br>
<br>
<b>Schools: </b>
<br>
Clicking add school and filling out the appropriate details creates a school and is saved to the database.
<br>
<br>
<b>Stats: </b>
<br>
Choose the appropriate school / client. This will be reflective of what work the employee has completed with the school. / client. A graph will show the relevant data.
<br>
<br>
<b>Email: </b>
<br>
Email part of the app is currently still under development.
<h1><b>Getting Started</b></h1>

1.	git clone https://github.com/yourusername/ed5-hrapp.git
2.	cd ed5-hrapp
3.	pip install -r requirements.txt
4.	python manage.py migrate
5.	python manage.py runserver





















































































