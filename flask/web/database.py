import psycopg2
import sys
import os



def connector():

    host = os.environ['POSTGRES_DB']
    dbname = os.environ['POSTGRES_DB']
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']

    con = None
    con = psycopg2.connect(host=host, dbname=dbname, user=user, password=password )
    return con