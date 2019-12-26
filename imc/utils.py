import datetime
from datetime import date


def get_profile_full_name(obj):
    return f'{obj.first_name} {obj.last_name}'


def get_profile_age(obj):
    return date.today().year - obj.date_of_birth.year


def format_date_of_birth(obj):
    return obj.date_of_birth.strftime('%d/%m/%Y')
