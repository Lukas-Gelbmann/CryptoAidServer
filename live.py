import shrimpy
import time
import pymongo
import json
import os

#get stored data
path = os.path.dirname(__file__)
exchangelist = json.load(open(path + "exchanges.json"))
credentials = json.load(open(path + "credentials.json"))

while True:
    try:
        #connect to db
        dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        db = dbclient["crypto"]
        print("Connected to DB")
        #connect to api
        client = shrimpy.ShrimpyApiClient(credentials['public_key'], credentials['secret_key'])

        #get exchanges
        print("--exchanges--")
        with dbclient.start_session() as session:
            session.start_transaction()
            mycol = db['exchanges']
            mycol.delete_many({})
            mycol.insert_many(exchangelist)
            session.commit_transaction()

        while True:
            with dbclient.start_session() as session:
                for exchange in exchangelist:
                    # get live ticker
                    print(exchange['exchange'])
                    print("--liveticker--")
                    data = client.get_ticker(exchange['exchange'])
                    session.start_transaction()
                    collection = db[exchange['exchange'] + "_ticker"]
                    collection.delete_many({})
                    collection.insert_many(data)
                    session.commit_transaction()
                    time.sleep(5)

                    # get orderbooks
                    print("--orderbooks--")
                    orderbooks = client.get_orderbooks(exchange['exchange'],limit=1)
                    session.start_transaction()
                    collection = db[exchange['exchange'] + "_orderbooks"]
                    collection.delete_many({})
                    collection.insert_many(orderbooks)
                    session.commit_transaction()
                    time.sleep(5)

    except Exception as e:
        print(e)
