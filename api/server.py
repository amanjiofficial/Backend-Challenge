from flask import Blueprint, request, flash
from flask_restful import Resource, Api
from api.db import db
from api.utility import UpdateRequestSchema, TicketSchema, generateID, retrieveExpiryTime, convertDateTime, validNoOfBooking, expiryTime, convertDateTimeReverse

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
                return {'error': 'Database could not be configured. Please try again later'}, 500
        
        return {'message': 'Congratulations booking Confirmed', 'ticketID': ticket["ticketID"]}, 201
    
    def get(self):
            if "timing" in request.args:
                if request.args["timing"] == '':
                    return {'error': 'Invalid value of timing'}, 400
                else:
                    timing = request.args["timing"]
                    print(timing)
                    response = []
                    try:
                        retrieveTickets = list(db.bookings.tickets.find({'timing': convertDateTime(timing) }))
                        for tickets in retrieveTickets:
                            tickets['expire'] = convertDateTimeReverse(retrieveExpiryTime(tickets['expire']))
                            tickets['timing'] = convertDateTimeReverse(tickets['timing'])
                            tickets['_id'] = str(tickets['_id'])
                            response.append(tickets)
                    except Exception as e:
                        flash(e.__str__())
                        return {'error': 'Database could not be configured. Please try again later'}, 500

                return {'tickets': response}, 200 
            else:
                try:
                    if request.args["ticketID"]:
                        if request.args["ticketID"] == '':
                            return {'error': 'Invalid value of ticket ID'}, 400
                        else:
                            ticketID = request.args["ticketID"]
                            try:
                                retrieveTicket = db.bookings.tickets.find_one({'ticketID': ticketID })
                                if not retrieveTicket:
                                    return {'error': "No ticket exists with this ticketID"}, 400
                                retrieveTicket['expire'] = convertDateTimeReverse(retrieveExpiryTime(retrieveTicket['expire']))
                                retrieveTicket['timing'] = convertDateTimeReverse(retrieveTicket['timing'])
                                retrieveTicket['_id'] = str(retrieveTicket['_id'])
                            except Exception as e:
                                print(e.__str__())
                                return {'error': 'Database could not be configured. Please try again later'}, 500

                        return {'ticket': retrieveTicket}, 200 
                except KeyError:
                    return {'error': 'Requires atleast ticketID or timing'}, 400

    def put(self):
        updateRequest = UpdateRequestSchema()
        errors = updateRequest.validate(request.args)
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
                ticket = db.bookings.tickets.find_one({'ticketID': request.args['ticketID'] })
                if not ticket:
                    return {'error': "No ticket exists with this ticketID"}, 400
                db.bookings.tickets.update_one({'ticketID': request.args['ticketID'] }, 
                {
                '$set': {
                    'timing': timing,
                    'expire': expiryTime(timing)
                    }
                })
            except Exception as e:
                flash(e.__str__())
                return {'error': 'Database could not be configured. Please try again later'}, 500
    
        return {'message': 'Ticket Details updated'}, 201

api.add_resource(TicketBooking, '/book')