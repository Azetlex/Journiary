# journal_project/urls.py

from django.contrib import admin
from django.urls import path, include   # Import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('journal.urls')),   # Include app-specific URLs
]
