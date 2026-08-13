from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    SignupView,
    LoginView,
    LogoutView,
    ProfileView,
    AdminDashboardView,
    SocialMediaView,
    ProductionCoordinatorView,
    ClientServicingView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('social-media/', SocialMediaView.as_view(), name='social-media'),
    path('production-coordinator/', ProductionCoordinatorView.as_view(), name='production-coordinator'),
    path('client-servicing/', ClientServicingView.as_view(), name='client-servicing'),
]
