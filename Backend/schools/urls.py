from django.urls import path
from . import views
from .views import AddSchoolsView

urlpatterns = [
    path('add_schools/', AddSchoolsView.as_view(), name='add_schools'),  
    
]
