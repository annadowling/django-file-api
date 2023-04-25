from django.urls import path
from file_app.views import upload_file, delete_file, get_file

urlpatterns = [
    path('upload_file', upload_file, name='upload_file'),
    path('delete_file', delete_file, name='delete_file'),
    path('get_file', get_file, name='get_file'),
]
