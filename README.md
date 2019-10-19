## fake-mongo

Populates a mongodb instance with fake data generated from a mongoke configuration.
`Str` generates alphanumeric garbage, to generate data that is somewhat readable you can use some of these aliases:
<--! to update use regex '(\w+)':.*, --->
```yml
Email: Str
FullName: Str
Name: Str
LastName: Str
Username: Str
Age: Int
Telephone: Str
Language: Str
DateTime: Any
Date: Any
Time: Any
TimeStamp: Any
Price: Str
Address: Str
City: Str
```

One example of config can be this:
```
# mongoke.yml
skema: |
    User:
        name: FirstName
        email: Email

    FirstName: Str
    Email: Str

types:
    User:
        collection: users
```

Run inside docker compose like this:
```yml
# docker-compose.yml
version: '3'
services:
    populate-db:
        image: mongoke/populate-mongo
        volumes:
            - ./mongoke.yml/:/conf.yml
        environment:
            - DB_URL=mongodb://mongo/db
    mongo:
        image: mongo
        ports:
        - 27017:27017
        logging: 
            driver: none
```