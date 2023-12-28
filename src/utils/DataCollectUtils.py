import datetime

"""
Get the week numbers for a given year period.

Parameters:
- year_period (list): A list of years for which to retrieve the week numbers.

Returns:
- list: A sorted list of unique week numbers in the format "YYYYWW".
"""


def get_week_numbers(year_period):
    week_numbers = set()
    for year in year_period:
        start_date = datetime.date(int(year), 1, 1)
        end_date = datetime.date(int(year), 12, 31)

        current_date = start_date
        while current_date <= end_date:
            _, iso_week, _ = current_date.isocalendar()
            week_numbers.add(int(f"{year}{iso_week:02d}"))
            current_date += datetime.timedelta(days=7)

    return sorted(week_numbers)
