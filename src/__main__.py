import yaml
from typing import *
import random
import os.path
import bson
from bson.objectid import ObjectId
import asyncio
from funcy import post_processing, merge, flatten
from skema.fake_data import fake_data
from skema.reconstruct import from_graphql
from mongoke.support import get_types_schema
# from mongoke.skema_support import get_type_properties, get_schema
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import Collection
from .resolvers import resolvers

CONF_PATH = os.getenv('CONF_PATH') or "/conf.yml"
DOCUMENTS_PER_COLLECTION = int(os.getenv('DOCUMENTS_PER_COLLECTION') or 20)
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    print("missing DB_URL from env")




def get_related_couples(config) -> Dict[str, set]:
    result: Dict[str, set] = {name: set() for name in config.get("types", {}).keys()}
    for relation in config.get("relations", []):
        x = relation["from"]
        y = relation["to"]
        result[x].add(y)
        result[y].add(x)
    
    return result

defaults_scalars = '''
ObjectId: Any
DateTime: Any
Date: Any
Time: Any
ID: Str
'''

default_graphql_scalars = '''
scalar ObjectId
'''

async def main(config, url):
    config = config or {}
    db: AsyncIOMotorClient = AsyncIOMotorClient(url).get_database()
    schema = get_types_schema(config, "/")
    schema = schema + default_graphql_scalars
    schema = from_graphql(schema)
    schema = schema + defaults_scalars
    object_ids_pool = {
        name: [bson.ObjectId() for i in range(DOCUMENTS_PER_COLLECTION)]
        for name, _ in config["types"].items()
    }
    print('object_ids_pool', list(object_ids_pool.keys()))
    connections = get_related_couples(config)
    for typename, config in config.get("types", {}).items():
        related_collections = connections[typename]
        if related_collections:
            ids = list(flatten([object_ids_pool[name] for name in related_collections]))
            print(f"generating object ids between {typename} and {related_collections}, from a pool of {len(ids)}")
            r = random.Random()
            def pick_id():
                id = r.choice(ids)
                # print(f'[{typename}] picking id {id} from {related_collections} pool')
                return id
            custom_resolvers_map = {"ObjectId": lambda: pick_id(), **resolvers}
        else:
            custom_resolvers_map = {"ObjectId": ObjectId, **resolvers}
        items = fake_data(
            schema,
            ref=typename,
            amount=DOCUMENTS_PER_COLLECTION,
            resolvers=custom_resolvers_map,
        )
        for idx, item in enumerate(items):
            if "_id" in item:
                item["_id"] = object_ids_pool[typename][idx]
        # print(dir(db[collection]))
        coll_name = config.get("collection", None)
        if coll_name:
            collection = db[coll_name]
            print(
                f"persisting {len(items)} documents in {collection.name} in db {collection.database.name}"
            )
            await collection.insert_many(items)


if __name__ == "__main__":
    if not os.path.exists(CONF_PATH):
        print("no configuration found at " + CONF_PATH)
        raise Exception()
    asyncio.run(main(yaml.safe_load(open(CONF_PATH)), url=DB_URL))

