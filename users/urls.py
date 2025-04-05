from django.urls import path
from .views import LoginView, RegistrationView, AdminDashboardStatusView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('admin/', AdminDashboardStatusView.as_view(), name='dashboard-stats')
]

