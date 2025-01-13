from django.urls import path
from . import views

app_name='bookings'

urlpatterns = [
    path('bookings/', views.bookings, name='bookings'),
    path('calendar/<str:month>/<int:year>/', views.calendar, name='calendar'),
    path('day/<str:date>/', views.dayview, name='dayview'),
    path('create_booking/', views.create_booking, name='create_booking'),
]