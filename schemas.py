"""List of schemas for Airline Route's related CSVs"""
from pyspark.sql.types import StructType

ROUTE_SCHEMA = StructType() \
    .add('airline', 'string') \
    .add('airline_id', 'string') \
    .add('source_airport', 'string') \
    .add('source_airport_id', 'string') \
    .add('destination_airport', 'string') \
    .add('destination_airport_id', 'string') \
    .add('codeshare', 'string') \
    .add('stops', 'integer') \
    .add('equipment', 'string')

AIRPORT_SCHEMA = StructType() \
    .add('airport_id', 'integer') \
    .add('name', 'string') \
    .add('city', 'string') \
    .add('country', 'string') \
    .add('iata', 'string') \
    .add('icao', 'string') \
    .add('latitude', 'float') \
    .add('longitude', 'float') \
    .add('altitude', 'float') \
    .add('timezone', 'string') \
    .add('dst', 'string') \
    .add('tz_database_time_zone', 'string') \
    .add('type', 'string') \
    .add('source', 'string')

AIRLINE_SCHEMA = StructType() \
    .add('airline_id', 'string') \
    .add('name', 'string') \
    .add('alias', 'string') \
    .add('iata', 'string') \
    .add('icao', 'string') \
    .add('callsign', 'string') \
    .add('country', 'string') \
    .add('active', 'string')
