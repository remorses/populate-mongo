## fake-mongo

Populates a mongodb instance with fake data generated from a mongoke configuration.
Also creates some random relations between types, following the relations field of the configurations puts a random ObjectId from one of the related collections in fileds of type ObjectId.


## Usage
To try an example run the docker-compose inside this repository
Another example:
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

## Fake Data
`Str` generates alphanumeric garbage, to generate data that is somewhat readable you can use some of these aliases:
<!-- to update use regex '(\w+)':.*, -->
```yml
Email: Str
FullName: Str
FirstName: Str
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

## Env Vars
- **`DB_URL`** the database url **with the database name**
- **`LOCALE`** default is "en", the locale used to generate the fake data, read more in [mimesis](https://mimesis.name/getting_started.html#supported-locales) documentation
- **`DOCUMENTS_PER_COLLECTION`**, default is 20, how many documents create for every collection

