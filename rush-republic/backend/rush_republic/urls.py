from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'online',
        'message': 'Rush Republic API is running successfully',
        'endpoints': {
            'signup': '/api/signup/',
            'login': '/api/login/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', health_check, name='root-health'),
    path('api/', health_check, name='api-health'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]


