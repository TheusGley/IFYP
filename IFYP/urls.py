
from django.contrib import admin
from django.urls import path,include
from bond.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bond.urls')),
    
]
