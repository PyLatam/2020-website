import json
import datetime
import attr
from bs4 import BeautifulSoup

from django.core.validators import validate_email


def to_date(value):
    return datetime.datetime.strptime(value, '%b %d %Y').date()


@attr.s
class Reservation:
    name = attr.ib()
    email = attr.ib()
    status = attr.ib()
    checkin = attr.ib(converter=to_date)
    checkout = attr.ib(converter=to_date)
    occupancy = attr.ib(type=int)

    @email.validator
    def check_email(self, attribute, value):
        validate_email(value)

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, features='lxml')
        data_field = soup.find(id='ctl00_content_JsonDisplay')

        if not data_field:
            raise ValueError('Invalid reservation')

        try:
            reservation_data = json.loads(data_field.attrs['value'])
            rooms = reservation_data['rooms']
        except (KeyError, ValueError, TypeError):
            raise ValueError('Unable to parse reservation')

        try:
            # Ensure the reservation is made for PyCon Latam
            assert 'PYCON LATAM CONGRESS' in rooms[0]['ratePlan']
        except (AssertionError, IndexError):
            raise ValueError('Invalid reservation')

        try:
            occupancy = sum(
                room['adults'] + room['childs'] + room['juniors']
                for room in rooms
            )
            reservation = cls(
                name=reservation_data['travelerInformation']['name'],
                email=reservation_data['travelerInformation']['mail'],
                status=reservation_data['hotelInformation']['status'],
                checkin=reservation_data['hotelInformation']['checkIn'],
                checkout=reservation_data['hotelInformation']['checkOut'],
                occupancy=occupancy,
            )
        except KeyError:
            raise ValueError('Unable to get traveler information')
        return reservation
