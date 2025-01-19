from django.db import models
from datetime import datetime, timedelta
from apps.accounts.models import User

class Day(models.Model):
  day_today = models.DateField(default=datetime.today)
  start_time = models.TimeField()
  finish_time = models.TimeField()
  slot_duration = models.IntegerField(default=20)
  holiday = models.BooleanField(default=False)

  def get_day_slots(self):
    slots = []
    current_time = datetime.combine(self.day_today, self.start_time)
    end_time = datetime.combine(self.day_today, self.finish_time)
    slot_delta = timedelta(minutes=self.slot_duration)

    while current_time < end_time:
      slots.append(current_time.time().strftime('%H:%M'))
      current_time += slot_delta
    
    return slots

  def __str__(self):
    return self.day_today.strftime('%A %b %d, %Y')


class Booking(models.Model):
  customer = models.ForeignKey(User, on_delete=models.CASCADE, default=999000) 
  artist = models.CharField(max_length=255, blank=True, null=True)  # Could be linked to a User model for staff
  service = models.CharField(max_length=255)  # To be refined when the Service model is ready
  updated_at = models.DateTimeField(auto_now=True)
  booking_date = models.DateField(default=datetime.today)
  start_time = models.TimeField()
  booked_slots = models.IntegerField(default=1)
  paid = models.BooleanField(default=False)
  comments = models.TextField(blank=True)

  def __str__(self):
    return f"{self.service} for {self.customer}"
    # return f"{self.service} for Admin"