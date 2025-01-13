from django.shortcuts import render
from django.urls import reverse
import calendar
from calendar import  HTMLCalendar
import datetime
from datetime import datetime,timedelta, time
from django.http import JsonResponse
import json
from django.contrib import messages
from  .temp_data import services_data
from . models import Day, Booking


# Create your views here.
def bookings(request):
  context = { }
  return render(request, 'bookings/booking.html', context)


# def calendar(request, year, month):
def calendar(request, year, month):
  month = month.capitalize()
  month_number = list(calendar.month_number).index(month)
  # month_number = int(month_number)
  html_cal = HTMLCalendar().formatmonth(
    year,
    month_number
  )
  context = {
    'year': year,
    'month': month,
    # 'month_number': month_number,
    'html_cal': html_cal
  }
  return render(request, 'bookings/calendar.html', context)



def dayview(request, date=None):
  """
  If Date is clicked from calander then date is passed to the dayview function. 
  If None then datetime.today().date() function takes the today's date as default
  """
  if date:
    date = str(date)
    day_date = datetime.strptime(date, '%d-%m-%Y').date()

  else:
    day_date = datetime.today().date() 

  # Convert the string times to datetime.time objects
  vendor_start_time = time(8, 00)
  vendor_finish_time = time(18,00)
  start_time = vendor_start_time
  finish_time = vendor_finish_time

  day, created = Day.objects.get_or_create(
    day_today=day_date, 
    start_time=start_time,
    finish_time=finish_time,
    slot_duration=20,
    holiday=False,)

  slots = day.get_day_slots()
  now = datetime.now()

  # print("day ==> ", day)
  #Filter available slots based on current time for today
  if day_date == now.date():
    print("(comming from dayview)   date for the day in question ==>",  day_date)
    current_time = now.time()
    slots = [slot for slot in slots if slot > str(current_time)]


  #Services to be retrieved from Service model using temp_data for now:
  services = []
  for service in services_data:
    services.append(service)
    
  bookings = Booking.objects.filter(booking_date=day.day_today, start_time__in=slots)
  # booked_slots = {b.start_time.strftime('%H:%M'): b for b in bookings}

  booked_slots = {}

  for booking in bookings:
    start_time = datetime.combine(day.day_today, booking.start_time)
    slot_delta = timedelta(minutes=day.slot_duration)
    
    # Mark the number of slots booked, starting from the start_time
    for i in range(booking.booked_slots):
      slot_time = (start_time + i * slot_delta).time().strftime('%H:%M')
      booked_slots[slot_time] = booking

  next_day = day_date + timedelta(days=1)
  prev_day = day_date - timedelta(days=1)

  context ={ 
    'services': services,
    'day': day,
    'slots': slots,
    'bookings':bookings,
    'booked_slots': booked_slots,
    'next_day_url': reverse('bookings:dayview', kwargs={'date': next_day.strftime('%d-%m-%Y')}),
    'prev_day_url': reverse('bookings:dayview', kwargs={'date': prev_day.strftime('%d-%m-%Y')}),

    }
  return render(request, 'bookings/dayview.html', context)

def create_booking(request):

  customer = request.user

  if request.method == 'POST':
    try:
      data = json.loads(request.body)

      try:
        booking_date = datetime.strptime(data['date'], '%A %b %d, %Y').date()
      except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

      service = data.get('service', {}).get('name')
      slot = data.get('slot')
      slots_number = data.get('service', {}).get('slotsnumber', 1)
      if not service or not slot:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

      # Create booking
      booking = Booking.objects.create(
        artist="any",
        service=service,
        booking_date=booking_date,
        start_time=slot,
        booked_slots=slots_number,
        paid=False,
        comments='capture from the userform',
      )
      booking.save()
      messages.success(request, "Booking Created Successfully")
      return JsonResponse({'message': 'Booking created successfully!'}, status=201)
    except Exception as e:
      print(f"Unhandled exception: {e}")
      messages.error(request, "There was an error")
      return JsonResponse({'error': str(e)}, status=400)

  return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


def bookings(request):
  return render(request, 'bookings/bookings.html')