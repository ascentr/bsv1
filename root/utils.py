from calendar import HTMLCalendar
import datetime
from typing import Any

class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, year: int, month: int):
        """ 
        Custom HTML Calendar to include year and month for the date URLs.

        Args:  
          year (int): The year for the calendar.
          month (int): The month for the calendar.
        """
        super().__init__()
        self.year = year
        self.month = month

    def formatday(self, day: int, weekday: int) -> str:
        """
        Return a formatted string for a single day in the calendar.
        
        Args:
          day (int): The day of the month.
          weekday (int): The weekday index (0 for Monday, etc.).

        Returns:
          str: An HTML string for the day.
        """
        # Today's date
        today = datetime.date.today()

        # If the day is not in the current month
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        # The date for the current cell
        current_date = datetime.date(self.year, self.month, day)

        # Generate the cell content
        if current_date < today:  # Past dates are not clickable
            return f'<td class="{self.cssclasses[weekday]}">{day}</td>'
        else:  # Current and future dates are clickable
            date_url = f"/selected_day/{day}-{self.month}-{self.year}/"
            return f'<td class="{self.cssclasses[weekday]}"><a href="{date_url}">{day}</a></td>'