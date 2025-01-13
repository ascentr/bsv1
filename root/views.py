from django.shortcuts import render
from datetime import datetime, time, timedelta
from .utils import CustomHTMLCalendar



def home(request):

  month = int(request.GET.get('month', datetime.now().month))
  year = int(request.GET.get('year', datetime.now().year)) 

  next_month = (month % 12) + 1
  prev_month = 12 if month == 1  else month -1
  
  next_year = year + (1 if month == 12 else 0)
  prev_year = year - (1 if month == 1 else 0)

  html_cal = CustomHTMLCalendar(year,month).formatmonth(year, month)

  context = {
    'year':year,
    'month':month,
    'html_cal':html_cal,
    'next_month' : next_month,
    'prev_month' : prev_month,
    'next_year' : next_year, 
    'prev_year' : prev_year,
  }

  return render(request, 'index.html', context)

