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
        # connect to db
        dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
        db = dbclient["crypto"]
        print("Connected to DB")
        # connect to api
        client = shrimpy.ShrimpyApiClient(credentials['public_key'], credentials['secret_key'])


        # get tradingpairs for exchange
        print("--tradingpairs--")
        tradingpairs = []
        with dbclient.start_session() as session:
            i = 0
            for exchange in exchangelist:
                print(exchange['exchange'])
                tradingpairs.append(client.get_trading_pairs(exchange['exchange']))
                time.sleep(2)
                session.start_transaction()
                mycol = db[exchange['exchange'] + "_tradingpairs"]
                mycol.delete_many({})
                mycol.insert_many(tradingpairs[i])
                session.commit_transaction()
                i = i + 1

        # get history
        while True:
            print("--history--")
            i = 0
            with dbclient.start_session() as session:
                for exchange in exchangelist:
                    print(exchange['exchange'])
                    for pair in tradingpairs[i]:
                        history = client.get_candles(exchange['exchange'], pair['baseTradingSymbol'], pair['quoteTradingSymbol'], '1d')
                        data = {"baseTradingSymbol": pair['baseTradingSymbol'], "quoteTradingSymbol": pair['quoteTradingSymbol'], "history": history}
                        print(pair)
                        time.sleep(5)
                        session.start_transaction()
                        mycol = db[exchange['exchange'] + "_history_1d"]
                        mycol.delete_many(pair)
                        mycol.insert_one(data)
                        session.commit_transaction()
                    i = i + 1

    except Exception as e:
        print(e)
