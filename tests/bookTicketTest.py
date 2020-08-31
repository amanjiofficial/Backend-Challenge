import pytest
from api import create_app
from api.db import dbtest

@pytest.mark.parametrize(('username', 'phoneNo', 'timing', 'message'), (
    ('', '', '', b'Username not provided'),
    ('test', '', '', b'Phone number not provided'),
    ('test', '9999999999', '', b'Timing not provided'),
    ('test', '9999999999', '2020-07-15T16:00', b'Ticket Booked successfully')
))
def testBookingEndpoint(client, username, phoneNo, timing, message):
    response = client.post(
        '/api/book',
        json = {'username': username, 'phoneNo': phoneNo, 'timing': timing }
    )
    dbtest.bookings.tickets.drop()
    assert message in response.data

def tesBookingLimit(client):
    response = ''
    for _ in range(21):
        response = client.post(
            '/api/book',
            json = {'name': 'test', 'phone': '999999999', 'timing': '2020-07-15T16:25'}
        )
    dbtest.bookings.tickets.drop()
    assert b'No more bookings allowed for this timing' in response.data