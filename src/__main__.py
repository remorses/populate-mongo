import yaml
import os.path
import bson
import asyncio
from funcy import post_processing
import skema
from mongoke.support import get_skema
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import Collection


CONF_PATH = '/conf.yml'
DB_URL = os.getenv('DB_URL')
if not DB_URL:
    print('missing DB_URL from env')

custom_resolvers = {
    'ObjectId': lambda: bson.ObjectId(),
}

async def main(config, url, custom_resolvers={}):
    db: AsyncIOMotorClient = AsyncIOMotorClient(url).get_database()
    schema = get_skema(config, '/')
    for typename, config in config['types'].items():
        items = skema.fake_data(schema, ref=typename, amount=10, resolvers=custom_resolvers)
        # print(dir(db[collection]))
        config = config or {}
        coll_name = config.get('collection', None)
        if coll_name:
            collection: Collection = db[coll_name]
            print(f'persisting {len(items)} documents in {collection.name} in db {collection.database.name}')
            await collection.insert_many(items,)


if __name__ == '__main__':
    if not os.path.exists(CONF_PATH):
        print('no configuration found at ' + CONF_PATH)
        raise Exception()
    asyncio.run(main(
        yaml.safe_load(open(CONF_PATH)),
        url=DB_URL,
        custom_resolvers=custom_resolvers
    ))