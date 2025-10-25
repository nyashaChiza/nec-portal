
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
    path('', RedirectView.as_view(url='/auth/login/', permanent=False)),
    path('optimus/', admin.site.urls),
    path('auth/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('farm/', include(('farm.urls', 'farm'), namespace='farm')),
    path('users/', include(('accounts.urls', 'user'), namespace='user')),
]
