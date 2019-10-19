import random
from prtty import pretty
from skema import fake_data
from bson.objectid import ObjectId

count = 0

def pick():
    return ObjectId()

resolvers = {
    'Random':  pick
}

schema = '''
X:
    r: Random
    s: Str
Random: Float
'''

pretty(fake_data(schema, ref='X', resolvers=resolvers))