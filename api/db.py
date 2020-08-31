from pymongo import MongoClient
from os import environ

db = MongoClient(environ.get('DB_URI'))
dbtest = MongoClient(environ.get('DB_TEST_URI'))