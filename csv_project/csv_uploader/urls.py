from django.urls import path
from .views import upload_csv, upload_success

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('success/', upload_success, name='upload_success'),
]
