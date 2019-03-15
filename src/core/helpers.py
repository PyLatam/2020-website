import requests

from bs4 import BeautifulSoup

from .datastructures import Reservation


def get_reservation(email, number):
    session = requests.Session()
    endpoint = 'https://secure.internetpower.com.mx/portals/FriendlyEng/hotel/secure/FindBooking.aspx'
    # Fetch session fields
    response_1 = session.get(endpoint)
    soup = BeautifulSoup(response_1.content, features='lxml')
    form = soup.find(id='aspnetForm')
    hidden_fields = form.select('input[type="hidden"]')
    form_data = {field.attrs['name']: field.attrs['value'] for field in hidden_fields}
    form_data['ctl00$content$txtEmail'] = email
    form_data['ctl00$content$txtNoReservation'] = number
    form_data['ctl00$content$Send'] = 'SEARCH'
    # Fetch reservation data
    response_2 = session.post(endpoint, data=form_data)

    try:
        reservation = Reservation.from_html(response_2.content)
    except ValueError:
        #TODO: Add logging
        reservation = None
    return reservation
