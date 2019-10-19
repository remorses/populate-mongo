from mimesis import Generic, Person, Business, Datetime, Text, Address

generic = Generic('en')
person = Person('en')
text = Person('en')
date = Datetime('en')
business = Business('en')
address = Address('en')

resolvers: dict = {
    'Email': person.email,
    'FullName': person.full_name,
    'Name': person.name,
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