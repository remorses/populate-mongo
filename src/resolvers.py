import os
from mimesis import Generic, Person, Business, Datetime, Text, Address

LOCALE = os.getenv('LOCALE') or 'env'

# generic = Generic(LOCALE)
person = Person(LOCALE)
text = Person(LOCALE)
date = Datetime(LOCALE)
business = Business(LOCALE)
address = Address(LOCALE)

resolvers: dict = {
    'Email': person.email,
    'FullName': person.full_name,
    'FirstName': person.name,
    'LastName': person.last_name,
    'Username': person.username,
    'Age': person.age,
    'Telephone': person.telephone,
    'Language': text.language,
    'DateTime': date.datetime,
    'Date': date.date,
    'Time': date.time,
    'TimeStamp': date.timestamp,
    'Price': business.price,
    'Address': address.address,
    'City': address.city,
}