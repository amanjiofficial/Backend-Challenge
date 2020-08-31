import datetime
from dateutil import tz
from marshmallow import Schema, fields
import random
import string
from .db import db

class TicketSchema(Schema):
    username = fields.Str(required=True)
    phoneNo = fields.Str(required=True)
    timing = fields.Str(required=True)

def convertDateTime(time):
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M")

def validNoOfBooking(timing):
    bookingCount = db.bookings.tickets.find({'timing': timing }).count()
    if bookingCount == 20:
        return False
    return True

def generateID():
    return "".join(random.choice("0123456789abcdef") for _ in range(32))

def expiryTime(timing):
    return timing.replace(tzinfo=tz.tzlocal()).astimezone(tz.tzutc()) + datetime.timedelta(hours=8)
