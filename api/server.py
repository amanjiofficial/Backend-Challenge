from flask import Blueprint, request, flash
from flask_restful import Resource, Api
from api.db import db
from api.utility import TicketSchema, generateID, convertDateTime, validNoOfBooking, expiryTime

bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint)

class TicketBooking(Resource):
    def post(self):
        ticket = TicketSchema()
        errors = ticket.validate(request.args)
        if errors:
            return (404, str(errors))
        else:
            try:
                timing = convertDateTime(request.args['timing'])
            except ValueError as v:
                return {'error': v.__str__()}
            try:
                if not validNoOfBooking(timing):
                    return {'error': 'Booking Full for this timing.'}, 400

                ticket = {
                    'ticketID': generateID(),
                    'expire': expiryTime(timing),
                    'username': request.args['username'].strip(),
                    'phoneNo': request.args['phoneNo'].strip(),
                    'timing': timing,
                }
                db.bookings.tickets.insert_one(ticket)
            except Exception as e:
                flash(e.__str__())
                return {'error': 'Database error. Please try again later'}, 500
        
        return {'message': 'Congratulations booking Confirmed', 'ticketID': ticket["ticketID"]}, 201

api.add_resource(TicketBooking, '/book')