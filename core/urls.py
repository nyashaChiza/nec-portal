
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
    path('optimus/', admin.site.urls),
    path('', RedirectView.as_view(url='/auth/login/', permanent=False)),
    path('auth/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
]
