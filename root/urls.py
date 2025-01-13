from django.contrib import admin
from django.urls import path, include
from . import views
from apps.bookings import views as vb

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    # path('selected_day/<str:date>/', views.selected_day, name="selected_day"),
    path('selected_day/<str:date>/', vb.dayview, name="selected_day"),
    path('accounts/', include('apps.accounts.urls')),
    path('bookings/', include('apps.bookings.urls')),
]
