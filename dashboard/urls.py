from django.urls import path
from dashboard.views import DashboardView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
#    path('admin-dash', AdminDashboardView.as_view(), name='admin_dashboard'),

]