from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token # Importe a view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cacambas.urls')),
    
    # Adicione esta linha para criar o endpoint de login
    path('api/login/', obtain_auth_token, name='api_token_auth'),
]