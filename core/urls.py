
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('optimus/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
]
